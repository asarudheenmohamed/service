"""Endpoint to get selected store driver orders."""
import logging

from rest_framework import viewsets
from rest_framework.response import Response
from app.core import serializers
from rest_framework.decorators import api_view

from app.store_manager.lib.store_order_controller import StoreOrderController

from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


authentication_classes = (StoreManagerAuthentication,)

@api_view(['GET'])
def store_orders(request):
    """Get all active state order objects.

    Input:
        store_id

    returns:
        return store_data(SalesFlatOrder Object)

    """
    store_id = request.GET['store_id']

    logger.debug('To Get driver order details of the store:{}'.format(
        store_id))

    controller = StoreOrderController()
    store_data = controller.store_orders(store_id)
    #  To Get SalesOrderSerializer data
    serializer_class = serializers.SalesOrderSerializer(store_data, many=True)

    logger.info('To Get driver order details of the store:{}'.format(
        store_id))

    return Response(serializer_class.data)




