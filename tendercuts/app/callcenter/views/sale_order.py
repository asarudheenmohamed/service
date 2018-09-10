"""Endpoint to provide store and order details."""
import logging

from rest_framework import viewsets

from app.core import serializers
from app.sale_order import models

from ..auth import CallCenterAuthentication

logger = logging.getLogger(__name__)


class SalesOrderDetailSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """

    authentication_classes = (CallCenterAuthentication,)
    # authentication_classes = (Ca,)
    # queryset = models.SalesFlatOrder.objects.all()
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        order_id = self.request.query_params['order_id']
        # .select_related("driver")       \
        queryset = models.SalesFlatOrder.objects \
            .filter(increment_id=order_id) \
            .order_by('-created_at') \
            .prefetch_related("items") \
            .prefetch_related("payment") \
            .prefetch_related("shipping_address")

        return queryset
