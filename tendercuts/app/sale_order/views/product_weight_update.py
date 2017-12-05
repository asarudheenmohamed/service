"""Endpoint for update the product weight."""
import datetime
import json
import logging
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from app.driver.auth import DriverAuthentication
from app.sale_order.lib.order_stat_controller import (OrderDataController,
                                                      StoreOrderController)
logger = logging.getLogger(__name__)


class OrderItemWeightUpdateViewSet(APIView):
    """Endpoint to update product weight.

    EndPoint:
        API: sale_order/item_weight/

    """
    authentication_classes = (DriverAuthentication,)

    def post(self, request, format=None):
        """Update the product weight.

        Input:
            items: order items
            increment_id: order increment_id

        returns:
            status(bol): weight update status

        """
        item_objects = self.request.data['items']
        controller = OrderDataController(self.request.data['increment_id'])
        logger.info(
            "To update the weight for this order:{} item".format(self.request.data['increment_id']))

        controller.item_weight_update(item_objects)

        return Response(
            {'status': True, 'message': 'successfully weight update'})
