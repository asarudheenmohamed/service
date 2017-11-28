"""Endpoint to create driver trip."""

import logging

from rest_framework import renderers, status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from app.core import serializers
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverTripViewSet(viewsets.GenericViewSet):
    """Enpoint to create the driver trip.

    EndPoint:
        API: driver/driver_trip/

    """
    authentication_classes = (DriverAuthentication,)

    def create(self, request, *args, **kwargs):
        """Create Driver Trip.

        Input:
            order_ids

        returns:
            Response({status: bool, message: str})

        """
        user_id = get_user_id(self.request)
        order_ids = self.request.data['order_ids']

        controller = DriverController.driver_obj(user_id)
        logger.info(
            'to create the trip for the given list of orders:{}'.format(order_ids))

        controller.create_driver_trip(order_ids)

        logger.info('trip created for that driver:{}'.format(user_id))

        return Response(
            {'status': True, "message": 'successfully trip created'})
