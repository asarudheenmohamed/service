"""Endpoint to get driver location details."""
import logging

from app.driver.serializer import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from app.store_manager.lib.store_order_controller import StoreOrderController
from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


authentication_classes = (StoreManagerAuthentication,)

@api_view(['GET'])
def driver_lat_lon(request):
    """Get driver current location.

    Input:
        phone_number

    returns:
        return driver_lat_lon(DriverLocation Object)

    """
    phone_number = request.GET['phone_number']
    #  To get driver object
    driver_obj = StoreOrderController.get_driver_obj(phone_number)

    logger.debug('To Get current location of driver:{}'.format(
      driver_obj))

    controller = StoreOrderController()
    driver_lat_lon = controller.get_driver_location(driver_obj)
    # Get DriverPositionSerializer data
    serializer_class = serializers.DriverPositionSerializer(driver_lat_lon)

    logger.info('Fetched driver:{} current location details'.format(
        driver_obj))

    return Response(serializer_class.data)

