"""Endpoint for update the product weight."""

import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from app.core import serializers
from ..auth import DriverAuthentication
from app.core.models.sales_order import SalesFlatOrderItem

logger = logging.getLogger(__name__)


class ProductWeightUpdateView(GenericAPIView, UpdateModelMixin):
    """Endpoint to update product weight.

    EndPoint:
        API: driver/product_weight/update/

    """
    authentication_classes = (DriverAuthentication,)
    queryset = SalesFlatOrderItem.objects.all()
    serializer_class = serializers.SalesFlatOrderItemSerializer

    def put(self, request, *args, **kwargs):

        update_obj = self.update(request, *args, **kwargs)

        logger.info(
            'Updated the weight for this item id:{}'.format(request.data['item_id']))

        return update_obj
