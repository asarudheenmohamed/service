from . import serializers as serializers
from . import models as models

from rest_framework.views import APIView
from rest_framework import viewsets, generics, mixins
import json
import datetime
from rest_framework.response import Response
from .lib import magento as magento
import itertools

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
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # queryset = models.CatalogProductFlat1.objects.all()
    # serializer_class = serializers.CatalogProductFlat1Serializer
    def get(self, request):
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

            _, product_ids, _ = zip(*records)

            data['products'] = [ products[pid] for pid in product_ids \
                    if pid in products]
            data['products'] = product_serializer(data['products'], many=True).data

            response.append(data)

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

    
            

    # @detail_route(methods=['post'])
    # def get(self, request, *args, **kwargs):
    #     otp = models.OtpList.objects.filter()

    #     if (len())
    #     return Response(snippet.highlighted)


