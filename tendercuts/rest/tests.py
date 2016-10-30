from django.test import TestCase
from rest.models import Order, GeoCoordinate, Leg, Route

class GeoCoordinates(TestCase):
    def setUp(self):
        route = Route.objects.create(total_distance=100, total_duration=200)
        source = Order.objects.create(
            order_id="1",
            route=route,
            coordinates=GeoCoordinate(lat="1.1", long="2"))

        destination = Order.objects.create(
            order_id="2",
            route=route,
            coordinates=GeoCoordinate(lat="1.2", long="2"))

        Leg.objects.create(distance=10, duration=560, source=source, destination=destination)

    def test_model_fetch(self):
        """Animals that can speak are correctly identified"""
        data = Order.objects.get(order_id="1")
        assert data.coordinates.lat == 1.1
#         self.assertEqual(lion.speak(), 'The lion says "roar"')

    def test_leg(self):
        leg = Leg.objects.get(source=Order.objects.get(order_id='1'))
        assert leg.duration == 560

    def test_route(self):
        route = Route.objects.get(pk=1)
        assert route.total_duration == 200
        assert len(route.orders.all()) == 2




