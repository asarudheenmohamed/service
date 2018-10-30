"""Endpoint to get selected store driver orders."""
import logging

from rest_framework import viewsets

from app.core import serializers
from app.core import models
from app.store_manager.lib import StoreBaseController
from rest_framework.pagination import  PageNumberPagination

from ..auth import StoreManagerPermission

# Get an instance of a logger
logger = logging.getLogger(__name__)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StoreOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active order objects.

    EndPoint:
        API: store_manager/store_data/

    """
    pagination_class = LargeResultsSetPagination
    permission_classes = (StoreManagerPermission,)
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        """Get all active state order objects.

        Input:
            store_id

        returns:
            return store_data(SalesFlatOrder Object)

        """
        store_id = self.request.GET['store_id']

        logger.debug('To Get driver order details of the store:{}'.format(
            store_id))

        controller = StoreBaseController(store_id)
        store_data = controller.get_current_orders(['pending', 'scheduled_order',
            'processing', 'out_delivery', 'complete'])

        return store_data


class HistoricOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all historic order objects.

    EndPoint:
        API: store_manager/order_history/

    """

    permission_classes = (StoreManagerPermission,)
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        """Get all active state order objects.

        Input:
            store_id

        returns:
            return store_data(SalesFlatOrder Object)

        """
        store_id = self.request.GET['store_id']

        filters  = {}
        for field_name, field_value in self.request.query_params.items():
            if field_name in ['page']:
                continue
            filters[field_name] = field_value

        return models.SalesFlatOrder.objects\
            .filter(**filters).order_by('-created_at')

