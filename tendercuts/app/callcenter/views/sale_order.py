"""Endpoint to provide store and order details."""
import logging

from rest_framework import viewsets
from typing import Optional, Any

from app.core import serializers
from app.sale_order import models
from app.driver.models import DriverOrder, DriverPosition, DriverTrip
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
        """TODO: Refactor this logic into controller and add unit test cases
        TODO: Add documentation.
        """

        waypoints = []
        current_order_id = self.request.query_params['order_id']

        current_order = DriverOrder.objects.filter(increment_id=current_order_id).first()

        # current driver position
        last_position = DriverPosition.objects.filter(driver_user=current_order.driver_user). \
            order_by('-recorded_time').first()  # type: DriverPosition
        waypoints.append({
            'latitude': last_position.latitude,
            'longitude': last_position.longitude
        })

        trip = DriverTrip.objects.filter(driver_order=current_order).first()
        increment_ids = trip.driver_order.values_list('increment_id', flat=True)

        if increment_ids:
            orders = models.SalesFlatOrder.objects.filter(increment_id__in=increment_ids) \
                        .prefetch_related("shipping_address")

            orders = list(orders)

            current_seq_no = 0
            for order in orders:  # type: models.SalesFlatOrder
                if current_order_id == order.increment_id:
                    current_seq_no = order.sequence_number

            for order in orders:  # type: models.SalesFlatOrder
                # skipping completed orders
                if order.status == 'complete':
                    continue

                if order.sequence_number >= current_seq_no:
                    break

                shipping_address = order.shipping_address.all().filter(
                    address_type='shipping').first()
                waypoints.append({
                    'latitude': shipping_address.o_latitude,
                    'longitude': shipping_address.o_longitude
                })

        return Response(waypoints)
