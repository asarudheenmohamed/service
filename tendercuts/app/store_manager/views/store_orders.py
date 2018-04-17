"""Endpoint to get selected store driver orders."""
import logging

from rest_framework import viewsets

from app.core import serializers
from app.store_manager.lib.store_order_controller import StoreOrderController

from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint to get all active order objects.

    EndPoint:
        API: store_manager/store_data/

    """

    authentication_classes = (StoreManagerAuthentication,)
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

        controller = StoreOrderController()
        store_data = controller.store_orders(store_id)

        return store_data
