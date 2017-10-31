import datetime
import json

from . import models
from . import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView

from app.sale_order.lib.order_data_controller import OrderDataController


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
                .order_by('-created_at')                    \
                .prefetch_related("items")                  \
                .prefetch_related("payment")                \
                .prefetch_related("shipping_address")       \
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
        
        express = models.ExpressDelivery().serialize()
        if express:
           data.append(express)

        return Response(data)


class OrderDataViewSet(APIView):
    """Endpoint to fetch order details.

    EndPoint:
        API: sales_order/order_data/

    """

    def get(self, request):
        """To get our order details.

        Input:
            order_id

        returns:
            Response(param_data)

        """
        order_id = self.request.GET['order_id']
        controller = OrderDataController(order_id)
        param_data = controller.order_details(order_id)

        return Response(param_data)
