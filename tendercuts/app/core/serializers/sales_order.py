from rest_framework import serializers
from .. import models as models
from .driver_serializer import DriverSerializer
from .store import StoreSerializer


class SalesOrderAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SalesFlatOrderAddress
        fields = ('fax', "street", "region", "city", 'postcode',
                  "telephone", "email", "address_type")


class SalesFlatOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SalesFlatOrderItem
        fields = (
            'item_id',
            "product_id",
            "name",
            "qty_ordered",
            "weight",
            "row_total"
        )


class SalesFlatOrderPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SalesFlatOrderPayment
        fields = ('method', )


class SalesOrderSerializer(serializers.ModelSerializer):
    shipping_address = SalesOrderAddressSerializer(many=True)
    items = SalesFlatOrderItemSerializer(many=True)
    payment = SalesFlatOrderPaymentSerializer(many=True)
    # driver = DriverSerializer()
    # store = StoreSerializer()
    # promised_delivery_time = serializers.SerializerMethodField('promised_delivery_time')

    class Meta:
        #'driver',
        model = models.SalesFlatOrder
        fields = ('entity_id', "increment_id", "customer_id",
                  "customer_firstname", "customer_firstname",
                  "grand_total", "updated_at", "payment",
                  "store_id", "shipping_address", "items",
                  "status", "order_now", "promised_delivery_time",
                  "promised_delivery_time_dt"
                  )
