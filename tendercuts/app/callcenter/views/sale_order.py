"""Endpoint to provide store and order details."""
import logging

from rest_framework import viewsets
from typing import Optional, Any

from app.core import serializers
from app.sale_order import models
from app.driver.models import DriverOrder, DriverPosition
from rest_framework import views
from rest_framework.response import Response

from ..auth import CallCenterPermission

logger = logging.getLogger(__name__)


class SalesOrderDetailSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """

    permission_classes = (CallCenterPermission,)
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


class SaleOrderLocationAPI(views.APIView):
    permission_classes = (CallCenterPermission,)

    def get(self, request):

        order_id = self.request.query_params['order_id']

        order = DriverOrder.objects.filter(increment_id=order_id).first()

        last_position = DriverPosition.objects.filter(driver_user=order.driver_user).\
            order_by('-recorded_time').first()  # type: DriverPosition

        return Response({
            'latitude': last_position.latitude,
            'longitude': last_position.longitude
        })
