"""Endpoint for  driver update the sequence number."""

import logging

from app.core import serializers
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.new_trip_controller import DriverTripController
from rest_framework import renderers, status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UpdateOrdersSequenceViewSet(viewsets.GenericViewSet):
    """Enpoint that driver update the sequence number.

    EndPoint:
        API: driver/update_sequence_number/

    """
    authentication_classes = (DriverAuthentication,)

    def create(self, request, *args, **kwargs):
        """Driver update order sequence number..

        Prams:
            order_id(int):order increment_id
            sequence_number(str): order sequence number

        Returns:
            Response({status: bool, message: str})

        """
        order_id = self.request.data['order_id']
        sequence_number = self.request.data['sequence_number']

        driver = self.request
        controller = DriverTripController(driver.user)

        try:
            controller.update_sequence_number(order_id, sequence_number)
            status = True
            message = "Order:{} Sequence number updated successfully".format(
                order_id)

            logger.info(message)

        except ValueError as e:
            status = False
            message = str(e)

        return Response({'status': status, "message": message})
