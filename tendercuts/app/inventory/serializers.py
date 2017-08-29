"""Serializer for the new Inventory model."""

from rest_framework import serializers
from app.core import models as models

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GraminventoryLatest
        fields = '__all__'
