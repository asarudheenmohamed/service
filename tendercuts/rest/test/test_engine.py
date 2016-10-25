
from rest.lib.models.point import DistributionCenter
from rest.lib.engine import Engine

class TestEngine:
    def test_kora(self, orders):
        print (len(orders))
        dist = DistributionCenter(orders[0].id, orders[0].lat, orders[1].long)

        eng = Engine(dist)
        routes = eng.generate_routes(orders[1:])
        assert len(routes) == 5

        # check if all orders area assigned
        assigned_orders = 0
        for route in routes:
            print(route)
            assert route.total_duration < 5400
            assigned_orders += len(route.points)

        # Each route will start with the distribution center
        assert assigned_orders == len(orders[1:]) + len(routes)

