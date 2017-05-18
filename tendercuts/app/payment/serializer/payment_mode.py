from rest_framework import serializers
from .. import models


class PaymentModeSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentMode
    """
    class Meta:
        """
        """
        model = models.PaymentMode
        fields = ('title', 'method', 'gateway_code', 'priority',
                  'gateway_code_level_1', 'subtitle', 'offers', 'order_id')

    def create(self, validated_data):
        """
        Over-riding create method to ensure we are creating a transient
        object.
        The default implementation creates an object in table, which is what
        we need.
        """
        return models.PaymentMode(**validated_data)
