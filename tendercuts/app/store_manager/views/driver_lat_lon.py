"""Endpoint to get driver location details."""
import logging

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.driver.serializer import serializers
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
        #  To get driver object
        driver_obj = StoreOrderController.get_driver_obj(phone_number)

        logger.debug('To Get current location of driver:{}'.format(
            driver_obj))

        controller = StoreOrderController()
        driver_lat_lon = controller.get_driver_location(driver_obj)

        # return as a list not an object
        return [driver_lat_lon]
