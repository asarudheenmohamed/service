"""Endpoint for  driver assignment."""

import logging
from rest_framework import renderers, status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from app.core import serializers
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController
from app.driver.models import DriverTrip


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
        # auto generated trip id
        trip_id = self.request.data.get('trip_id', None)

        driver = self.request
        controller = DriverController(driver.user)

        try:
            logger.debug(
                'To assign the order:{} to the driver:{}'.format(
                    order_id, driver.user.username))
            controller.assign_order(order_id, store_id, lat, lon, trip_id)
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
        trip_id = self.request.data.get('trip_id', None)
        force_complete = self.request.data.get('force_complete', None)
        # only if the trip is started the user should be able to
        # complete
        if trip_id:
            trip = DriverTrip.objects.get(pk=trip_id)
            if trip.status != DriverTrip.Status.STARTED.value:
                return Response({'status': False},
                                status=status.HTTP_403_FORBIDDEN)

        controller = DriverController(self.request.user)
        status_, message = controller.complete_order(
            order_id, lat, lon, trip_id,force_complete=force_complete)
        logger.info("status:{} message:{}".format(status_, message))

        return Response({'status': status_, 'message': message}, status=status.HTTP_201_CREATED)


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
        trip_id = self.request.query_params.get('trip_id', None)
        logger.info(
            'To fetch the Driver:{} assigning {} state orders'.format(
                user_id, status))

        return DriverController(self.request.user).fetch_orders(
            status, trip_id=trip_id)
