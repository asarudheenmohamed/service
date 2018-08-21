"""All GoogleApi controller related actions."""

import logging

from django.conf import settings
from app.core.models import SalesFlatOrder, SalesFlatOrderAddress
from app.core.models.customer.address import CustomerAddressEntity
import googlemaps
from app.core.models.store import CoreStore

logger = logging.getLogger(__name__)


class GoogleApiController(object):
    """GoogleApi controller."""

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
            self.logger.error(
                '{}, order_id:{}'.format(
                    repr(msg),
                    self.order.increment_id))

            # send error message in tech support mail
            Mail().send(
                "reports@tendercuts.in",
                ["tech@tendercuts.in"],
                "[CRITICAL] Error in Order ETA computaion",
                message)

        return direction_obj

    def _get_customer_geohash_location(self):
        """Returns the customer Address object and geohash location.
        """
        shipping_address = self.order.shipping_address.all().last()

        address_obj = CustomerAddressEntity.objects.filter(
            entity_id=shipping_address.customer_address_id).last()
        geohash_obj = address_obj.varchars.filter(
            attribute__attribute_code='geohash')

        if geohash_obj:
            address_texts_obj = address_obj.varchars.filter(
                attribute__attribute_code__in=['latitude', 'longitude']).values('attribute__attribute_code', 'value')
            lat_and_lng = {text_obj['attribute__attribute_code']: text_obj[
                'value'] for text_obj in address_texts_obj}

            self.logger.info('Fetched the geohash location:{},{} for the customer:{} order:{}'.format(
                lat_and_lng['latitude'], lat_and_lng['longitude'], self.order.customer_id, self.order.increment_id))

            return lat_and_lng, address_obj

        return False, False

    def compute_eta(self):
        """Update eta for customer location to store location."""

        geo_location, address_obj = self._get_customer_geohash_location()
        if geo_location:
            designated_store = address_obj.varchars.filter(
                attribute__attribute_code='designated_store').values('value').last()
            store_lat_and_lng = CoreStore.objects.filter(
                name=designated_store['value']).values(
                'location__longandlatis__longitude',
                'location__longandlatis__latitude').last()

            origin = "{},{}".format(
                store_lat_and_lng['location__longandlatis__latitude'],
                store_lat_and_lng['location__longandlatis__longitude'])

            destination = '{},{}'.format(
                geo_location['latitude'],
                geo_location['longitude'])
        else:
            origin = "{},{}".format(
                self.order.store.location.longandlatis.latitude,
                self.order.store.location.longandlatis.longitude)

            street_obj = address_obj.texts.filter(
                attribute__attribute_code='street').last()
            street = street_obj.value.strip('\n')

            if len(street) <= 1:
                post_code_obj = address_obj.varchars.filter(
                    attribute__attribute_code='postcode').last()
                destination = post_code_obj.value
            else:
                destination = street[1]

        directions = self.get_directions(origin, destination)

        eta = directions[0]['legs'][0]['duration']['value'] / 60

        SalesFlatOrderAddress.objects.filter(parent=self.order).update(eta=eta)

        self.logger.info('ETA time updated for the customer:{} order:{}'.format(
            self.order.customer_id, self.order.increment_id))
