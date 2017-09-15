"""Endpoints to provide driver events update status."""

import logging

from rest_framework import viewsets
from rest_framework.response import Response

from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverPositionViewSet(viewsets.ModelViewSet):
    """Fetch Driver order events and update driver position."""
    authentication_classes = (DriverAuthentication,)

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

        controller = DriverController.driver_obj(user_id)
        driver_position = controller.record_position(order_id, lat, lon)

        logger.info(
            '{}: Driver current location details updated'.format(user_id))

        return Response(
            {'status': True, 'message': 'driver location updated successfully'})
