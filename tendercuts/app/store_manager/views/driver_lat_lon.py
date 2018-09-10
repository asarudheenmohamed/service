"""Endpoint to get driver location details."""
import logging

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.driver.serializer import serializers
from app.store_manager.lib.store_order_controller import StoreOrderController

from ..auth import StoreManagerPermission

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint to fetch driver details.

    EndPoint:
        API: store_manager/driver_lat_lon/

    """

    permission_classes = (StoreManagerPermission,)
    serializer_class = serializers.DriverPositionSerializer

    def get_queryset(self):
        """Get driver current location.

        Input:
            phone_number

        returns:
            return driver_lat_lon(DriverLocation Object)

        """
        driver_id = self.request.GET['driver_id']
        #  To get driver object

        logger.debug('To Get current location of driver:{}'.format(
            driver_id))

        controller = StoreOrderController()
        driver_lat_lon = controller.get_driver_location(driver_id)

        # return as a list not an object
        return [driver_lat_lon]
