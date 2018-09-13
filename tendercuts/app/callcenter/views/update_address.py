"""Endpoint to provide store and order details."""
import logging

from rest_framework import views, response

from app.core import models
from app.core.lib.order_controller import OrderAddressController
from app.core.lib.user_controller import CustomerAddressController
from ..auth import CallCenterPermission

logger = logging.getLogger(__name__)


class UpdateAddressApi(views.APIView):
    """Update the customer's lat, lng and geohash details
    """
    permission_classes = (CallCenterPermission,)

    def post(self, request):
        """
        :param request:
            (order_id) - Increment id
            (lat) - Latitude
            (lng) - Longitude
            (geohash) - geohash precision
            (street) - google address

        :return: Response(True)
        """
        order_id = self.request.data['order_id']
        lat = self.request.data['lat']
        lng = self.request.data['lng']
        geohash = self.request.data['geohash']
        street = self.request.data['street']

        order = models.SalesFlatOrder.objects.filter(
            increment_id=order_id).first()  # type: models.SalesFlatOrder

        shipping_address = order.shipping_address.all().filter(address_type='shipping').first()
        OrderAddressController(order).update_address(
            geohash=geohash,
            lat=lat,
            lng=lng,
            street=street
        )
        
        address = models.CustomerAddressEntity.objects.filter(entity_id=shipping_address.customer_address_id).first()
        # update the customer address first
        CustomerAddressController(address).update_address(
            geohash=geohash,
            lat=lat,
            lng=lng,
            street=street
        )


        return response.Response({'status': True})
