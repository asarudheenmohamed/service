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
        store = CoreStore.objects.get(store_id=store_id)
        odoo_store = StockWarehouse.objects.get(mage_code=store.code)

        store_data = StoreSerializer(instance=store).data
        odoo_data = StockWarehouseSerializer(
            instance=odoo_store).data

        store.update(odoo_data)

        return Response(store_data)
