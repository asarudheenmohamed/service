from rest.lib.models.route import Leg, PseudoRoute, Route
import mock
import pytest

@pytest.fixture
def mock_orders():
    return [mock.MagicMock(name="order-{}".format(i)) for i in range(10)]

@pytest.fixture
def mock_legs(mock_orders):
    mock_legs= []
    for src, dest in zip(mock_orders, mock_orders[1:] + [mock_orders[0]]):
        mock_leg = mock.MagicMock()
        mock_leg.source = src
        mock_leg.destination = dest
        mock_leg.destination.unassigned_route = mock.MagicMock()

        mock_leg.duration = 35 * 60
        mock_legs.append(mock_leg)

    return mock_legs


class TestLeg:
    def test_leg_init(self, mock_orders):
        leg = Leg(mock_orders[0], mock_orders[1], 1, 1)
        assert leg.duration == 1

class TestPseudoRoute:
    def test_capacity(self, mock_orders):
        route = PseudoRoute(mock_orders[0])
        # First order should always be accepted
        assert route.can_add(route.max_capacity + 1)
        route.add_point(mock_orders[0], route.max_capacity + 1)

        # second rejected
        assert not route.can_add(route.max_capacity + 1)

    def test_capacity_success(self, mock_orders):
        route = PseudoRoute(mock_orders[0])
        # First order should always be accepted
        assert route.can_add(route.max_capacity/2 )
        route.add_point(mock_orders[0], distance=(route.max_capacity/60/2))

        # second accepted
        # 1200 => the point buffer for each order, so mulitplied by 2
        assert (route.can_add(route.max_capacity/2 - 1200))


# Other two test case ??
class TestRoute:
    def test_from_pseudo_route(self, mock_orders, mock_legs):
        """
        1. Check if 2 points are added
        2. check if unassigned is being called on all the rest of orders
        """
        p_route = PseudoRoute(mock_orders)

        gapi_mock = mock.MagicMock()
        gapi_mock.get_route.return_value = mock_legs

        route = Route.from_psuedo_route(p_route, gapi_mock)
        assert len(route.points) == 3

        for order in mock_orders[2:]:
            assert order.unassigned_route.called_once_with()


