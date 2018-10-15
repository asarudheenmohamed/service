"""Endpoint to get selected store driver orders."""
import datetime
import logging

from rest_framework import viewsets, mixins

from app.inventory.models import InventoryRequest
from app.inventory.serializers import InventoryRequestSerializer
from app.inventory.lib import InventoryRequestController
from app.store_manager.lib import InventoryFlockAppController
from app.core.lib import drf
from ..auth import StoreManagerPermission, InventoryManagerPermission

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreInventoryRequestApi(drf.CreateListMixin, mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active trip objects.

    EndPoint:
        GET & POST: store_manager/inv_request/

    """

    permission_classes = (StoreManagerPermission,)
    serializer_class = InventoryRequestSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            for record in request.data:
                record['triggered_by'] = request.user.id

        inv_request = super(StoreInventoryRequestApi, self).create(request, *args, **kwargs)

        # extract and get the inv reuqest obj.
        ids = map(lambda req: req['id'], inv_request.data)
        auto_approve_req = InventoryRequest.objects.filter(id__in=ids, qty__gt=0)

        # auto approve other requests
        for req in auto_approve_req:
            req.status = InventoryRequest.Status.APPROVED.value
            message = "Approved by {}".format(self.request.user.email)
            InventoryRequestController(req).process_request(message=message)

        if auto_approve_req:
            auto_approve_req.update(status=InventoryRequest.Status.APPROVED.value)
            InventoryFlockAppController(auto_approve_req).publish_request(
                template=InventoryFlockAppController.AUTO_TEMPLATE)

        approve_req = InventoryRequest.objects.filter(id__in=ids, qty=0)
        if approve_req:
            InventoryFlockAppController(approve_req).publish_request()


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

    def perform_update(self, serializer):
        """Override to handle inventory processing"""
        request = serializer.save()
        message = "Approved by {}".format(self.request.user.email)
        InventoryRequestController(request).process_request(message=message)
    
    def update(self, request, *args, **kwargs):
        request.data['approved_by'] = request.user.id
        return super(StoreInventoryApprovalApi, self).update(request, *args, **kwargs)
