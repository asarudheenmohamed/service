from rest_framework import serializers
from app.core.models.customer.address import CustomerAddressEntityVarchar


class CustomerAddressVarcharSerializer(serializers.ModelSerializer):
    """Serializer for the  CustomerAddressEntityVarchar model"""
    class Meta:
        model = CustomerAddressEntityVarchar
        fields = "__all__"
