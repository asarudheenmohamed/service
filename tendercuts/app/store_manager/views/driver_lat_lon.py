"""Endpoint to get driver location details."""
import logging

from app.driver.serializer import serializers
from rest_framework import viewsets
from app.store_manager.lib.store_order_controller import StoreOrderController
from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint to fetch driver details.

    EndPoint:
        API: store_manager/driver_lat_lon/

    """
    authentication_classes = (StoreManagerAuthentication,)
    serializer_class = serializers.DriverPositionSerializer

    def get_queryset(self):
    	"""Get driver current location.

        Input:
            phone_number

        returns:
            return driver_lat_lon(DriverLocation Object)
    	"""
        phone_number = self.request.GET['phone_number']
   		# convert unicode to string
        phone_number = phone_number.encode("ascii")

        controller = StoreOrderController()
        # get driver object by using phone number
        driver = controller.get_driver_id(phone_number)

        logger.debug('To Get current location of driver:{}'.format(
        	driver))

        driver_lat_lon = controller.get_driver_location(driver)

        return driver_lat_lon