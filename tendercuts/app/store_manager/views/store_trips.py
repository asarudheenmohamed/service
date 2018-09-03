"""Endpoint to get selected store driver orders."""
import logging

from rest_framework import viewsets, mixins

from app.driver import serializer as driver_serializer
from app.store_manager.lib import StoreBaseController

from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreTripViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active trip objects.

    EndPoint:
        API: store_manager/trips/

    """

    authentication_classes = (StoreManagerAuthentication,)
    serializer_class = driver_serializer.DrivertripSerializer

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
