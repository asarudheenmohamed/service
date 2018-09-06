from rest_framework import serializers

from app.geohashing.models import StockWarehouse



class StockWarehouseSerializer(serializers.ModelSerializer):
    # reverse link
    class Meta:
        model = StockWarehouse
        fields = ('name', "code", "mage_code", "flock_group_id", "path_strin")
