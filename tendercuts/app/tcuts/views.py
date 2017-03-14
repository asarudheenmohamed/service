from . import serializers as serializers
from . import models as models

from rest_framework.views import APIView
from rest_framework import viewsets, generics
import json
import datetime
from rest_framework.response import Response
from .core import magento_api as magento

from rest_framework import status


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    queryset = models.CoreStore.objects.all()
    serializer_class = serializers.StoreSerializer


class ProductViewSet(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    def get(self, request, format=None):
        products = models.ProductStore().get_store_product()

        return Response(products)


class CartAddApi(APIView):
    def post(self, request):

        product_id = self.request.data['product_id']
        qty = self.request.data['quantity']

        mage = magento.Connector()
        status = mage.api.tendercuts_order_apis.addToCart(
            product_id,
            qty)

        print(status)

        return Response(status)

