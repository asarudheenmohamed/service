
from rest.lib.engine import Engine
import rest.models as models
import pytest

class TestEngine:
    @pytest.mark.django_db
    def test_kora(self, orders):
        dist = orders[0]

        eng = Engine(dist)
        routes = eng.generate_routes(orders[1:])
        assert len(routes) == 5

        # check if all orders area assigned
        assigned_orders = 0
        for route in routes:
            print(route.total_duration)
            print (route.orders.all())
            assert route.total_duration < 5400
            assigned_orders += len(route.points)

        # Each route will start with the distribution center
        assert assigned_orders == len(orders[1:]) + len(routes)
        print (models.Order.objects.all()[0].route)

