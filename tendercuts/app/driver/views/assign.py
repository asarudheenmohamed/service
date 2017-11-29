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

    def create(self, request, *args, **kwargs):
        """Driver assignment  endpoint.

        Input:
            order_id

        returns:
            Response({status: bool, message: str})

        """
        order_id = self.request.data['order_id']
        store_id = self.request.data['store_id']
        lat = self.request.data['latitude']
        lon = self.request.data['longitude']

        user_id = get_user_id(self.request)
        controller = DriverController(user_id)

        try:
            controller.assign_order(order_id, store_id, lat, lon)
            status = True
            message = "Order Assigned successfully"
            logger.info(
                '{} this order assigned successfully'.format(
                    order_id))
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
        lat = self.request.data['latitude']
        lon = self.request.data['longitude']
        user_id = get_user_id(self.request)
        controller = DriverController(user_id)

        controller.complete_order(order_id, lat, lon)

        logger.info("{} this order completed successfully".format(order_id))

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

        logger.info(
            'Fetch {} state orders'.format(status))

        return DriverController(user_id).fetch_orders(status)
