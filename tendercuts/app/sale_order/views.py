"""Endpoint to provide store and order details."""
import datetime
import json
import logging

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.sale_order.lib.order_stat_controller import (OrderDataController,
                                                      StoreOrderController)

from . import models, serializers

logger = logging.getLogger(__name__)


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

        logger.info("Fetched the order details for given ordeer_id:{}".format(
            order_id))

        return Response(param_data)


class StoreDataViewSet(APIView):
    """Endpoint to fetch store order details.

    EndPoint:
        API: sales_order/store_order/

    """

    def get(self, request):
        """To get our order details.

        params:
            request:
                1.store_id(int) : Store id
                2.deliverydate(DateTimeField): Order's delivery date
                3.sku(str) : Product sku name
        returns:
            Response(order_list)

        """
        store_id = self.request.GET['store_id']
        deliverydate = self.request.GET['deliverydate']
        sku = self.request.GET['sku']
        controller = StoreOrderController(store_id)
        sku_order = controller.store_details(store_id, deliverydate, sku)

        logger.debug("Fetched scheduled_order's sku quantity details at date: {}".format(
                deliverydate))

        return Response(sku_order)
