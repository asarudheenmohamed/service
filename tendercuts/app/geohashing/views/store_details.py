"""Endpoint for the finding store mage_code with geohash,lat,lng."""
import logging

from app.core.models import CoreStore
from app.core.serializers import StoreSerializer

from app.geohashing.models import StockWarehouse
from app.geohashing.serializers import StockWarehouseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger()

class StoreDetailView(APIView):
    """/geohash/stores
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        """
        Url: geohash/store

        Return Modified version of store serializer
        """

        stores = CoreStore.objects.all()
        odoo_stores = StockWarehouse.objects.all()

        store_data = StoreSerializer(instance=stores, many=True).data
        odoo_data = StockWarehouseSerializer(instance=odoo_stores, many=True).data
        odoo_data = {store['mage_code']:store for store in odoo_data}

        for store in store_data:
            mage_code = store['code']
            if mage_code in odoo_data:
                store.update(odoo_data[mage_code])

        return Response(store_data)
