from rest_framework import serializers
from .. import models


class PaymentModeSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentMode, only used during the cart
    checkout process.

    TODO: clean me, architecturally this is incorrect.
    """
    class Meta:
        """
        """
        model = models.PaymentMode
        fields = ('title', 'subtitle', 'method', 'gateway_code',
                  'gateway_code_level_1', 'priority', 'offers', 'order_id',
                  'pin', 'expiry_month', 'expiry_year', 'brand', 'persist')

    def create(self, validated_data):
        """
        Over-riding create method to ensure we are creating a transient
        object.
        The default implementation creates an object in table, which is what
        we need.
        """
        return models.PaymentMode(**validated_data)

