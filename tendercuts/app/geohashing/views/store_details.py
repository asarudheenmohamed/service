"""Endpoint for the finding store mage_code with geohash,lat,lng."""

from app.core.models import CoreStore
from app.core.serializers import StoreSerializer

from app.geohashing.models import StockWarehouse
from app.geohashing.serializers import StockWarehouseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class StoreDetails(APIView):
    """/geohash/stores
    """

    def get(self, request, format=None):
        """
        Url: geohash/store

        Return Modified version of store serializer
        """

        stores = CoreStore.objects.all()
        odoo_stores = StockWarehouse.objects.all()

        store_data = StoreSerializer(instance=stores, many=True).data
        store_data.update(
            StockWarehouseSerializer(instance=odoo_stores, many=True).data)

        return Response(JSONRenderer().render(store_data))
