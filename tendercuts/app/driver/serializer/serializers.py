from rest_framework import serializers
from app.driver.models.driver_order import DriverStat, DriverTrip, DriverOrder
from app.core.serializers.sales_order import SalesOrderSerializer


class DriverStatSerializer(serializers.ModelSerializer):
    """
    Serializer for DriverPosition
    """
    class Meta:
        """
        """
        model = DriverStat
        fields = ('driver_id', 'no_of_orders')


class DriverOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for DriverOrder
    """
    class Meta:
        """
        """
        model = DriverOrder
        fields = ('driver_user', 'increment_id', 'created_at')


class DrivertripSerializer(serializers.ModelSerializer):
    """Serializer for DriverTrip."""
    driver_order = DriverOrderSerializer(many=True)

    class Meta:
        """
        """
        model = DriverTrip
        fields = (
            'driver_order',
            'driver_user',
            'km_travelled',
            'trip_created_time',
            'trip_ending_time',
            'trip_completed')
