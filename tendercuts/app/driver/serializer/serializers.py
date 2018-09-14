from rest_framework import serializers
from app.driver.models.driver_order import DriverStat, DriverTrip, DriverOrder, DriverPosition
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


class DriverPositionSerializer(serializers.ModelSerializer):
    """Serializer for DriverPosition."""

    class Meta:
        """
        """
        model = DriverPosition
        fields = ('latitude', 'longitude', 'driver_user', 'recorded_time')


class DrivertripSerializer(serializers.ModelSerializer):
    """Serializer for DriverTrip."""
    driver_order = DriverOrderSerializer(many=True, read_only=True)
    driver_position = DriverPositionSerializer(many=True, read_only=True)

    class Meta:
        """
        """
        model = DriverTrip
        fields = (
            'id',
            'driver_order',
            'driver_user',
            'km_travelled',
            'trip_created_time',
            'trip_ending_time',
            'trip_completed',
            'driver_position',
            'auto_assigned',
            'status'
        )

    def create(self, validated_data):
        """:Override: To handle implicit many to many creation."""
        trip = DriverTrip.objects.create(**validated_data)  # type: DriverTrip

        if 'driver_order' in self.initial_data:
            for order in self.initial_data.get('driver_order'):
                order = DriverOrder.objects.create(increment_id=order)
                trip.driver_order.add(order)
            trip.save()

        return trip
