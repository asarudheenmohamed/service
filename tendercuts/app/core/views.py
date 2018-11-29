import datetime
import itertools
import json
import logging

from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import list_route

from app.core.lib.controller import ProductsPriceController
from app.core.models.product import CatalogProductFlat1
from app.core.models.customer.address import CustomerAddressEntityVarchar

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


class CoreConfigDataViewSet(viewsets.ReadOnlyModelViewSet):
    """Return the Store address querysets.
    """
    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.CoreConfigDataSerializer

    def get_queryset(self):
        """Return to the store address objects."""

        queryset = models.CoreConfigData.objects.filter(
            path="general/store_information/address", scope="stores")

        return queryset


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
                if category_id == DEALS_ID and product[
                    'special_price'] is None:
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


class CustomerAddressVarcharViewSet(viewsets.ReadOnlyModelViewSet):
    """This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for AddressEntityVarchar

    Params:
     address_id(str): customer address entity id

    """
    serializer_class = serializers.CustomerAddressVarcharSerializer

    def get_queryset(self):
        """Return to the customer designated store objects."""
        address_id = self.request.query_params['address_id']

        queryset = CustomerAddressEntityVarchar.objects.filter(
            attribute_id=231, entity_id=address_id)

        return queryset


class CmsViewSet(viewsets.GenericViewSet):
    """A simple ViewSet for viewing Rating Tags.
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    @list_route(methods=['get'])
    def cms_title(self, request, pk=None):
        """List the CMS titles."""
        queryset = models.CmsPage.objects.filter(
            is_active=True).values(
            'title', 'page_id')

        return Response(queryset)

    @list_route(methods=['get'])
    def cms_page(self, request, pk=None):
        """Returns the CMS page object for give title."""
        page_id = self.request.query_params['page_id']
        queryset = models.CmsPage.objects.filter(page_id=page_id)
        serializer = serializers.CmsSerializer(queryset, many=True)

        return Response(serializer.data)


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


from django.db import connection


class ProductMetaApi(APIView):
    """Fetches and gives the API data."""
    authentication_classes = ()
    permission_classes = ()

    # the query is a bit complex, so using direct now.
    QUERY = """select
	product.entity_id, 
	meta_keyword.value keyword, 
	meta_description.value description,
	meta_title.value as title
from
catalog_product_entity product
left join catalog_product_entity_text meta_keyword on product.entity_id = meta_keyword.entity_id and meta_keyword.attribute_id = 83 and meta_keyword.store_id = 1
left join catalog_product_entity_varchar meta_description on product.entity_id = meta_description.entity_id and meta_description.attribute_id = 84 and meta_description.store_id = 1
left join catalog_product_entity_varchar meta_title on product.entity_id = meta_title.entity_id and meta_title.attribute_id = 82 and meta_title.store_id = 1"""

    def get(self, request):
        data = []
        with connection.cursor() as cursor:
            cursor.execute(self.QUERY)

            for pid, keyword, description, title in cursor.fetchall():
                data.append({
                    'product_id': pid,
                    'keyword': keyword,
                    'descrption': description,
                    'title': title
                })

        return Response(data)
