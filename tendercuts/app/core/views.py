import datetime
import itertools
import json
import logging

from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.controller import ProductsPriceController
from app.core.models.product import CatalogProductFlat1

from . import models as models
from . import serializers as serializers
from .lib import magento as magento

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    queryset = models.CoreStore.objects.all()
    serializer_class = serializers.StoreSerializer


class ProductViewSet(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    # queryset = models.CatalogProductFlat1.objects.all()
    # serializer_class = serializers.CatalogProductFlat1Serializer
    def get(self, request):
        DEALS_ID = 17
        store_id = self.request.GET['store_id']

        try:
            category = getattr(
                models,
                "CatalogCategoryFlatStore{}".format(store_id))

            products = getattr(
                models,
                "CatalogProductFlat{}".format(store_id))

            category_seralizer = getattr(
                serializers,
                "CatalogCategoryFlatStore{}Serializer".format(store_id))

            product_serializer = getattr(
                serializers,
                "CatalogProductFlat{}Serializer".format(store_id))
        except Exception as e:
            print(e)
            return Response(
                {"status": "No such store"},
                status=status.HTTP_400_BAD_REQUEST)

        categories_map = models.CatalogCategoryProduct.objects.all() \
                .order_by("category_id").values_list()
        categories_map = itertools.groupby(categories_map, key=lambda x: x[0])

        # TODO: NEED TO MOVE IT TO CONSTANTS
        # Fetch only visible & active item
        products = {p.entity_id: p for p in products.objects.all() 
                if p.status == 1 and p.visibility == 4}

        # Fetch all categories
        category = {c.entity_id: c for c in category.objects.all()
                if c.is_active == 1 and c.entity_id != 2}

        response = []
        for category_id, records in categories_map:
            # skip inactive cats
            if category_id not in category:
                continue

            data = {}
            data['category'] = category_seralizer(category[category_id]).data

            data['products'] = []
            for _, pid, sort_order in records:
                if pid not in products:
                    continue

                product = products[pid]
                product = product_serializer(product).data

                # inject sort order into the product.
                product['sort_order'] = int(sort_order)

                # if a deal(spl price) is enabled, only then we push in products
                # for DEALS category.
                if category_id == DEALS_ID and product['special_price'] is None:
                    continue
                else:
                    data['products'].append(product)

            # Skip empty cats, eg deals
            if len(data['products']) == 0:
                continue

            response.append(data)

        # what;s new will be in the beginning
        sort_order = [17]

        def sorter(x, y):
            xindex = yindex = 99

            try:
                xindex = sort_order.index(x['category']['entity_id'])
                yindex = sort_order.index(y['category']['entity_id'])
            except ValueError:
                pass

            return cmp(xindex, yindex)

        response.sort(sorter)

        return Response(response)



class CartAddApi(APIView):
    def post(self, request):

        product_id = self.request.data['product_id']
        qty = self.request.data['quantity']

        mage = magento.Connector()
        status = mage.api.tendercuts_order_apis.addToCart(
            product_id,
            qty)

        return Response(status)


class CustomerDataApi(APIView):
    def get(self, request):

        user_id = self.request.query_params['user_id']
        data = models.Customer().get_data(user_id)

        return Response(data)


class ProductPriceViewSet(APIView):
    """Endpoint to get product price details.

    EndPoint:
        API: core/product_price/

    """

    authentication_classes = ()
    permission_classes = ()
    
    def get(self, request):
        """Get Products prices for current store.

        Input:
            store_id

        return:
            Response(products_prices: dict)
        """
        store_id = self.request.GET['store_id']

        controller = ProductsPriceController()

        logger.debug(
            'To get product prices for current store:{}'.format(
                store_id))

        products_prices = controller.get_products_price(store_id)

        return Response(products_prices)
