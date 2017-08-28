"""Serializer for the new Inventory model."""

from rest_framework import serializers
from app.core import models as models

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GraminventoryLatest
        fields = ('product_id', 'qty', 'scheduledqty', 'parent', 'store_id', 'kg_qty', 'kg_expiring', 'kg_forecast', 'gpu')
