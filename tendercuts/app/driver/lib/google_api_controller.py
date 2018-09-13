"""All GoogleApi controller related actions."""

import logging

from django.conf import settings
import googlemaps
import geopy
from django.db.models import QuerySet

from app.core.models import SalesFlatOrder, SalesFlatOrderAddress, CoreStore
from app.driver.models import GoogleGeocode, GoogleAddressLatLng
from app.core.lib.communication import Mail

logger = logging.getLogger(__name__)


class GoogleApiController(object):
    """GoogleApi controller."""
    order = None  # type: SalesFlatOrder

    def __init__(self, order):
        """Constructor.

        Params:
          order: sale order

        """
        self.order = order
        self._api = googlemaps.Client(
            key=settings.GOOGLE_MAP_DISTANCE_API['KEY'])
        self.logger = logger

    def get_directions(self, origin, destination):
        """Fetch the directions for the origin to destination.

        Args:
            origin(str): location starting point
            destination_point(str): destination for order
        returns:
            return the google directions

          """
        direction_obj = self._api.directions(
            origin=origin, destination=destination)

        return direction_obj

    def _geocode(self, query):
        """Triggers a query to geocode also stores the result for caching."""
        data = GoogleGeocode.objects.filter(query=query)

        if data:
            logging.info("Got a cache hit for {}".format(query))
            return data.first()

        result = self._api.geocode(query)
        result = result[0]

        if 'bounds' in result['geometry']:
            vp = result['geometry']['bounds']
        else:
            vp = result['geometry']['viewport']

        n1, e1, s1, w1 = \
            vp['northeast']['lat'], vp['northeast']['lng'], vp[
                'southwest']['lat'], vp['southwest']['lng']

        height_ = geopy.distance.geodesic((n1, e1), (s1, e1)).km
        width_ = geopy.distance.geodesic((s1, w1), (s1, e1)).km
        area = (height_ * width_)
        geo = result['geometry']

        logging.info("Resolved {} to {}".format(query, area))

        return GoogleGeocode.objects.create(
            location_type=geo['location_type'],
            latitude=geo['location']['lat'],
            longitude=geo['location']['lng'],
            area=area,
            query=query
        )

    def resolve_address(self, fax, mage_street):
        """Tries to resolve the address to an approximate lat & lng."""

        logging.info('Resolving for {} & {}'.format(fax, mage_street))
        possibilities = []
        components = mage_street.split('\n')
        user_entered = components[0]
        google_addr = components[1] if len(components) >= 2 else None

        # Add fax
        if fax and len(fax) > 0:
            user_entered_address = "{}, {}".format(fax, user_entered)
        else:
            user_entered_address = user_entered

        search_string = []
        for street in reversed(user_entered_address.split(",")):
            street = street.strip()
            if not street:
                continue

            search_string.insert(0, street)

            if google_addr:
                street = "{}, {}".format(
                    ",".join(search_string), google_addr)
            else:
                street = ",".join(search_string)

            logging.info('Resolving for {}'.format(street))

            try:
                geocode = self._geocode(street)
            except Exception as e:
                logging.warning(str(e))
                continue

            if geocode.area < 0.1:
                possibilities.append(geocode)

        return self._get_best_match(possibilities)

    def _get_best_match(self, possibilities):
        """Private method to get the best geocode data.
        Currently we look for the last rooftop, geo center in this prio"""
        for geocode in reversed(possibilities):  # type: GoogleGeocode
            if geocode.location_type == 'ROOFTOP':
                return geocode.latitude, geocode.longitude

            if geocode.location_type == 'GEOMETRIC_CENTER':
                return geocode.latitude, geocode.longitude

    def compute_eta(self):
        """Update eta for customer location to store location."""

        shipping_address = self.order.shipping_address.all()
        shipping_address = shipping_address.filter(address_type='shipping').first()   # type: SalesFlatOrderAddress

        store_lat_and_lng = CoreStore.objects.filter(
            store_id=self.order.store_id).values(
            'location__longandlatis__longitude',
            'location__longandlatis__latitude').first()

        origin = "{},{}".format(
            store_lat_and_lng['location__longandlatis__latitude'],
            store_lat_and_lng['location__longandlatis__longitude'])

        if shipping_address.geohash:
            lat = shipping_address.o_latitude
            lng = shipping_address.o_longitude
        else:  # Non geohashed resolution.
            # fetch from cache if present.
            address_lat_lng = GoogleAddressLatLng.objects.filter(
                address_id=shipping_address.customer_address_id)  # type: QuerySet[GoogleAddressLatLng]

            if address_lat_lng:
                address_lat_lng = address_lat_lng.first()
                lat, lng = address_lat_lng.latitude, address_lat_lng.longitude
            else:
                # approx match
                try:
                    lat, lng = self.resolve_address(
                        shipping_address.fax, shipping_address.street)
                    GoogleAddressLatLng.objects.create(
                        address_id=shipping_address.customer_address_id,
                        latitude=lat,
                        longitude=lng)
                except Exception as msg:
                    message = 'Error for {} id: {} ({}: {}), message:{}'.format(
                        self.order.increment_id,
                        shipping_address.customer_address_id,
                        shipping_address.fax,
                        shipping_address.street,
                        repr(msg))

                    # send error message in tech support mail
                    Mail().send(
                        "reports@tendercuts.in",
                        ["jira@tendercuts.atlassian.net", "tech@tendercuts.in"],
                        "[INFO] Address resolution failed for customer",
                        message)

        destination = '{},{}'.format(lat, lng)

        directions = self.get_directions(origin, destination)

        legs = directions[0]['legs']
        shipping_address.eta = legs[0]['duration']['value'] / 60

        # if original lat and lng is missing, then we use the data from
        # directions api.
        if not shipping_address.o_longitude:
            logger.info("Info updating lat lng for {}".format(shipping_address.customer_address_id))
            shipping_address.o_latitude = lat
            shipping_address.o_longitude = lng
        shipping_address.save()

        self.logger.info('ETA time updated for the customer:{} order:{}'.format(
            self.order.customer_id, self.order.increment_id))
