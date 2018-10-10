"""Serializer for the new Inventory model."""

from rest_framework import serializers
from app.core import models as models
from app.inventory.models import NotifyCustomer, InventoryRequest


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GraminventoryLatest
        fields = '__all__'


class NotifyCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifyCustomer
        fields = '__all__'


class InventoryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryRequest
        fields = '__all__'
