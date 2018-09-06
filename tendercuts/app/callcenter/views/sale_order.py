"""Endpoint to provide store and order details."""
import datetime
import json
import logging

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.sale_order.lib.order_stat_controller import (OrderDataController,
                                                      StoreOrderController)
from app.sale_order import models
from app.core import serializers

logger = logging.getLogger(__name__)


class SalesOrderDetailSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """

    # authentication_classes = (Ca,)
    # queryset = models.SalesFlatOrder.objects.all()
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        try:
            order_id = self.request.query_params['order_id']
            # .select_related("driver")       \
            queryset = models.SalesFlatOrder.objects \
                           .filter(increment_id=order_id) \
                           .exclude(status__in=['canceled', 'closed']) \
                           .order_by('-created_at') \
                           .prefetch_related("items") \
                           .prefetch_related("payment") \
                           .prefetch_related("shipping_address")
        except KeyError:
            queryset = []

        return queryset


