from rest_framework import serializers
from app.driver.models.driver_order import DriverStat, DriverTrip
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


class DrivertripSerializer(serializers.ModelSerializer):
    """Serializer for DriverTrip."""

    class Meta:
        """
        """
        model = DriverTrip
        fields = (
            'driver_order',
            'driver_user',
            'km_traveled',
            'trip_created_time',
            'trip_ending_time',
            'trip_completed')
