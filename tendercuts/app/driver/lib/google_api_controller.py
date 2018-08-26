"""All GoogleApi controller related actions."""

import logging

from django.conf import settings
import googlemaps

from app.core.models import SalesFlatOrder, SalesFlatOrderAddress
from app.core.models.store import CoreStore
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
        try:
            direction_obj = self._api.directions(
                origin=origin, destination=destination)

            self.logger.info(
                'Fetch the Google directions for the origin:{} to destination:{}'.format(
                    origin, destination))

        except Exception as msg:
            message = 'Error:{}, origin:{},destination:{}'.format(
                repr(msg), origin, destination)

            # send error message in tech support mail
            Mail().send(
                "reports@tendercuts.in",
                ["tech@tendercuts.in"],
                "[CRITICAL] Error in Order ETA computation",
                message)

        return direction_obj

    def compute_eta(self):
        """Update eta for customer location to store location."""

        shipping_address = self.order.shipping_address.all().last()  # type: SalesFlatOrderAddress

        store_lat_and_lng = CoreStore.objects.filter(
            store_id=self.order.store_id).values(
            'location__longandlatis__longitude',
            'location__longandlatis__latitude').last()

        origin = "{},{}".format(
            store_lat_and_lng['location__longandlatis__latitude'],
            store_lat_and_lng['location__longandlatis__longitude'])

        if shipping_address.geohash:
            destination = '{},{}'.format(
                shipping_address.o_latitude, shipping_address.o_longitude)
        else:

            # Try to get the eta using street address
            street = shipping_address.street
            street = street.value.strip('\n')

            if len(street) <= 1:
                destination = shipping_address.postcode
            else:
                destination = street[1]

        data = {}
        directions = self.get_directions(origin, destination)

        legs = directions[0]['legs']
        data['eta'] = legs[0]['duration']['value'] / 60

        # if original lat and lng is missing, then we use the data from
        # directions api.
        if not shipping_address.o_longitude:
            data['o_latitude'] = legs[0]['end_location']['lat']
            data['o_longitude'] = legs[0]['end_location']['lng']

        shipping_address.update(**data)

        self.logger.info('ETA time updated for the customer:{} order:{}'.format(
            self.order.customer_id, self.order.increment_id))
