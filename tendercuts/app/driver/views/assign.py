"""Endpoint for  driver assignment."""

import logging

from rest_framework import renderers, status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from app.core import serializers
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController
from app.driver.lib.driver_position_update import DriverLocations
from app.driver.models.driver_order import DriverOrder

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
        lat = self.request.data['latitude']
        lon = self.request.data['longitude']
        driver = self.get_driver()
        controller = DriverController(driver)

        try:
            controller.assign_order(order_id, store_id)
            driver = DriverOrder.objects.get(
                driver_id=driver.customer.entity_id, increment_id=int(order_id))
            driver_location = DriverLocations(driver)
            obj = driver_location.update_driver_position(order_id, lat, lon)

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
        driver = self.get_driver()
        driver = DriverOrder.objects.filter(
            driver_id=driver.customer.entity_id, increment_id=order_id)
        controller = DriverController(driver[0])
        controller.complete_order(order_id)

        driver_location = DriverLocations(driver[0])
        driver_location.update_driver_position(order_id, lat, lon)

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

        return DriverController(driver).fetch_orders(status)
