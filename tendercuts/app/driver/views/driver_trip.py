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
        order_ids = self.request.data['order_ids']
        # get the user id
        user_id = get_user_id(self.request)
        # initialize the driver id in driver controller
        controller = DriverController(user_id)
        logger.info(
            'To create the trip with the given list of orders:{} for the driver:{}'.format(order_ids, user_id))

        controller.create_driver_trip(order_ids)

        return Response(
            {'status': True, "message": 'successfully trip created'})

    @list_route(methods=['post'], renderer_classes=[renderers.JSONRenderer])
    def complete(self, request, *args, **kwargs):
        """Driver order complete endpoint.

        Input:
            order_id

        Returns:
            Response({status: bool, message: str})

        """
        order_ids = self.request.data['order_ids']
        user_id = get_user_id(self.request)
        controller = DriverController(user_id)

        controller.complete_driver_trip(order_ids)

        logger.info("{} this order completed successfully".format(order_ids))

        return Response({'status': True}, status=status.HTTP_201_CREATED)
