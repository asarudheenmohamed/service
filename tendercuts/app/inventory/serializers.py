"""Serializer for the new Inventory model."""

from rest_framework import serializers
from app.core import models as models
from app.inventory.models import NotifyCustomer

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GraminventoryLatest
        fields = '__all__'

class NotifyCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifyCustomer
        fields = '__all__'
