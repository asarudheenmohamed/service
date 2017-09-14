"""Endpoint for  driver unassignment."""

import logging

from rest_framework import viewsets
from rest_framework.response import Response

from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication

logger = logging.getLogger(__name__)


class UnassignOrdersViewSet(viewsets.GenericViewSet):
    """Enpoint that unassigns driver to order.

    EndPoint:
        API: driver/unassign/

    """
    authentication_classes = (DriverAuthentication,)

    def get_driver(self):
        """Extract DriverId from request."""
        user_id = get_user_id(self.request)
        driver = CustomerSearchController.load_by_id(user_id)

        return driver

    def create(self, request, *args, **kwargs):
        """Driver unassignment endpoint.

        Input:
            order_id

        returns:
            Response({status: bool, message: str})

        """
        unassign_order_id = self.request.data['order_id']
        driver = self.get_driver()
        controller = DriverController(driver)
        try:
            controller.unassign_order(unassign_order_id)

            status = True
            message = 'Order unassigned successfully'

            logger.info(
                '{} this order unassigned successfully'.format(
                    unassign_order_id))

        except ValueError as e:
            logger.info(
                'Unable to assingn the order: {} to the driver:{}. Details: {}'.format(
                    unassign_order_id, str(e)))
            status = False
            message = str(e)

        return Response({'status': status, 'message': message})
