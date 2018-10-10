"""Endpoint for the finding store mage_code with geohash,lat,lng."""
import logging

from app.core.models import CoreStore
from app.core.serializers import StoreSerializer

from app.geohashing.models import StockWarehouse
from app.geohashing.serializers import StockWarehouseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger()


class StoreDetailView(APIView):
    """/geohash/store_details
    """

    def get(self, request, format=None):
        """
        Url: geohash/store_details

        Return Modified version of store serializer
        """
        store_id = request.user.userprofile.store_id
        if not store_id:
            stores = CoreStore.objects.all()
        else:
            stores = CoreStore.objects.get(store_id__in=store_id.split(','))
        
        
        codes = [store.code for store in stores]
        odoo_stores = StockWarehouse.objects.filter(mage_code__in=codes)

        store_data = StoreSerializer(instance=stores, many=True).data
        odoo_data = StockWarehouseSerializer(
            instance=odoo_stores).data

        odoo_data = {store['mage_code']:store for store in odoo_data}

        for store in store_data:
            mage_code = store['code']
            if mage_code in odoo_data:
                store.update(odoo_data[mage_code])

        return Response(store_data)
