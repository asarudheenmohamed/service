from rest_framework import serializers
from rest.models import Route, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id', 'location')

class RouteSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)
    class Meta:
        model = Route
        fields = ('total_duration', 'total_distance', 'orders')
