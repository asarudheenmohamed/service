from rest_framework import serializers
from app.driver.models.driver_order import DriverStat


class DriverStatSerializer(serializers.ModelSerializer):
    """
    Serializer for DriverPosition
    """
    class Meta:
        """
        """
        model = DriverStat
        fields = ('driver_id', 'no_of_orders')
