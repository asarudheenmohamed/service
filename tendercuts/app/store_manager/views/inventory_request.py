"""Endpoint to get selected store driver orders."""
import datetime
import logging

from rest_framework import viewsets, mixins

from app.inventory.models import InventoryRequest
from app.inventory.serializers import InventoryRequestSerializer
from app.store_manager.lib import InventoryFlockAppController
from ..auth import StoreManagerPermission, InventoryManagerPermission

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreInventoryRequestApi(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active trip objects.

    EndPoint:
        GET & POST: store_manager/inv_request/

    """

    permission_classes = (StoreManagerPermission,)
    serializer_class = InventoryRequestSerializer

    def create(self, request, *args, **kwargs):
        request.data['triggered_by'] = request.user.id
        inv_request = super(StoreInventoryRequestApi, self).create(request, *args, **kwargs)

        # extract and get the inv reuqest obj.
        inv_request_obj = InventoryRequest.objects.get(pk=inv_request.data['id'])
        InventoryFlockAppController(inv_request_obj).publish_request()

        return inv_request

    def get_queryset(self):
        """Get all active state trip objects.

        Input:
            store_id

        returns:
            return store_data(DriverTrip Object)

        """
        user = self.request.user

        today = datetime.date.today()
        requests = InventoryRequest.objects.filter(
            triggered_by=user,
            created_time__gt=today
        )

        return requests


class StoreInventoryApprovalApi(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active trip objects.

    EndPoint:
        GET & PUT: store_manager/pending_inv_requests/
              PUT: store_manager/pending_inv_requests/<id>

    """

    permission_classes = (InventoryManagerPermission,)
    serializer_class = InventoryRequestSerializer

    def get_queryset(self):
        """Get all active inventory requests.
        """
        today = datetime.date.today()
        requests = InventoryRequest.objects.filter(
            created_time__gt=today,
            status=InventoryRequest.Status.CREATED.value
        )

        return requests
