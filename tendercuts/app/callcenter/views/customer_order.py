import logging

from rest_framework import viewsets
from ..auth import CallCenterPermission


from app.core import models
from app.core import serializers

logger = logging.getLogger(__name__)


class SalesOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides the list of orders placesd by the customer.

    /callcenter/customer_orders/
    """

    # queryset = models.SalesFlatOrder.objects.all()
    permission_classes = (CallCenterPermission,)
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        try:
            user_id = self.request.query_params['user_id']
            # .select_related("driver")       \
            queryset = models.SalesFlatOrder.objects \
                           .filter(customer_id=user_id) \
                           .exclude(status__in=['canceled', 'closed']) \
                           .order_by('-created_at') \
                           .prefetch_related("items") \
                           .prefetch_related("payment") \
                           .prefetch_related("shipping_address")[:10]

        except KeyError:
            queryset = []

        return queryset
