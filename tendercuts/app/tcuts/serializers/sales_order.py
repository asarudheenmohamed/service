from rest_framework import serializers
from .. import models as models
from .driver_serializer import DriverSerializer

class SalesOrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalesFlatOrderAddress
        fields = ('fax', "street", "region", "city", 'postcode', "telephone", "email")


class SalesFlatOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SalesFlatOrderItem
        fields = ('item_id', "name", "qty_ordered", "row_total")


class SalesOrderSerializer(serializers.ModelSerializer):
    shipping_address = SalesOrderAddressSerializer()
    items = SalesFlatOrderItemSerializer(many=True)

    driver = DriverSerializer()

    class Meta:
        model = models.SalesFlatOrder
        fields = ('entity_id', "increment_id",
            "customer_firstname", "customer_firstname",
            "grand_total", "updated_at",
            "shipping_address", 'driver', "items")


