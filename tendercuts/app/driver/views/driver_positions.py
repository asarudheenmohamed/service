
"""Endpoints to provide Driver Events or status."""

import logging
from rest_framework import viewsets
from rest_framework.response import Response
from app.core.lib.utils import get_user_id
from app.driver.models.driver_order import DriverOrder, OrderEvents
from app.driver.serializer.serializers import OrderEventsSerializer
from app.driver.lib.geo_locations import GeoLocations
from app.driver.lib.driver_controller import DriverController
from ..auth import DriverAuthentication
# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverPositionViewSet(viewsets.ModelViewSet):
    """Fetch Driver order events and update driver position."""
    authentication_classes = (DriverAuthentication,)
    serializer_class = OrderEventsSerializer

    def get_queryset(self):
        """Fetch Driver order Events."""
        order_id = self.request.GET.get('order_id')
        user_id = get_user_id(self.request)

        obj = OrderEvents.objects.filter(
            driver=DriverOrder.objects.filter(
                driver_id=user_id, increment_id=order_id))

        return obj

    def create(self, request, *args, **kwargs):
        """update the driver locations.

        params:
         latitude(int): driver location latitude
         longitude(int): driver location longitude

        Returns:
            status

        """
        order_id = self.request.data['order_id']
        lat = self.request.data['latitude']
        lon = self.request.data['longitude']
        user_id = get_user_id(self.request)

        driver_obj = DriverOrder.objects.filter(
            driver_id=user_id, increment_id=order_id)
        controller = DriverController(driver_obj[0])
        driver_position = controller.driver_position(lat, lon)
        logger.info("Find the driver locations")
        location = GeoLocations()
        location = location.get_location(lat, lon)

        sales_obj = controller.get_order_obj(driver_obj[0].increment_id)

        obj = controller.order_events(
            location, sales_obj.status)
        logger.info("Driver order events updated")

        return Response(
            {'status': True, 'message': 'driver location updated successfully'})
