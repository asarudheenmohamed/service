"""Endpoint for  driver assignment."""

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


class DriverOrdersViewSet(viewsets.GenericViewSet):
    """Enpoint that assigns driver to order.

    EndPoint:
        API: driver/assign/
        API: driver/assign/complete

    """
    authentication_classes = (DriverAuthentication,)

    def get_driver(self):
        """Extract DriverId from request."""
        user_id = get_user_id(self.request)
        driver = CustomerSearchController.load_by_id(user_id)

        return driver

    def create(self, request, *args, **kwargs):
        """Driver assignment  endpoint.

        Input:
            order_id

        returns:
            Response({status: bool, message: str})

        """
        order_id = self.request.data['order_id']
        store_id = self.request.data['store_id']
        driver = self.get_driver()
        controller = DriverController(driver)

        try:
            controller.assign_order(order_id,store_id)
            status = True
            message = "Order Assigned successfully"
        except ValueError as e:
            status = False
            message = str(e)

        return Response({'status': status, "message": message})

    @list_route(methods=['post'], renderer_classes=[renderers.JSONRenderer])
    def complete(self, request, *args, **kwargs):
        """Driver order complete endpoint.

        Input:
            order_id

        Returns:
            Response({status: bool, message: str})

        """
        order_id = self.request.data['order_id']

        driver = self.get_driver()
        controller = DriverController(driver)
        controller.complete_order(order_id)

        return Response({'status': True}, status=status.HTTP_201_CREATED)


class OrderFetchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Endpoint to provide a list for sales orders

    """
    authentication_classes = (DriverAuthentication,)
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        """Return a query set containing all sale order of the driver."""
        user_id = get_user_id(self.request)
        driver = CustomerSearchController.load_by_id(user_id)
        status = self.request.query_params['status']

        return DriverController(driver).fetch_orders(status)
