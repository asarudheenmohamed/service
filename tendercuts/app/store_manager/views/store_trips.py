"""Endpoint to get selected store driver orders."""
import logging

from app.driver import serializer as driver_serializer
from app.store_manager.lib import StoreBaseController, StoreOrderController
from rest_framework import mixins, renderers, status, viewsets
from rest_framework.response import Response

from ..auth import StoreManagerPermission

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreTripViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active trip objects.

    EndPoint:
        API: store_manager/trips/

    """

    permission_classes = (StoreManagerPermission,)
    serializer_class = driver_serializer.DrivertripSerializer

    def create(self, request, *args, **kwargs):
        """Driver assignment  endpoint.

        Params:
            request dict object like {"driver_user":2343546, "driver_order": [100043454,1000032423]}

        returns:
            Response({status: bool, message: str})

        """

        status_,message=StoreOrderController().store_manager_assign_orders(request.data)

        return Response(
                {'status': status_, 'message': message},
                 status=status.HTTP_201_CREATED)


    def get_queryset(self):
        """Get all active state trip objects.

        Input:
            store_id

        returns:
            return store_data(DriverTrip Object)

        """
        store_id = self.request.GET['store_id']

        controller = StoreBaseController(store_id)
        store_data = controller.get_current_trips()

        return store_data
