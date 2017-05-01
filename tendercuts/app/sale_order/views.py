import datetime
import json

from . import models
from . import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView



class SalesOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # queryset = models.SalesFlatOrder.objects.all()
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        try:
            user_id = self.request.query_params['user_id']
                # .select_related("driver")       \
            queryset = models.SalesFlatOrder.objects        \
                .filter(customer_id=user_id)                \
                .exclude(status__in=['canceled', 'closed']) \
                .order_by('-created_at')                     \
                .prefetch_related("items")                  \
                .prefetch_related("payment")                \
                .prefetch_related("shipping_address")                 \
                [:10]

        except KeyError:
            queryset = []

        return queryset

class DeliveryViewSet(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # queryset = models.CatalogProductFlat1.objects.all()
    # serializer_class = serializers.CatalogProductFlat1Serializer

    def get(self, request):
        data = []
        data.append(models.ScheduledDelivery().serialize())
        data.append(models.ExpressDelivery().serialize())

        return Response(data)



