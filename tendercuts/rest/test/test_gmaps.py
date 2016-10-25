from rest.lib.models import route
from rest.lib import gmaps

def _test_get_distance(orders):
    maps = gmaps.GMaps()
    nearby_orders, distances, times = maps.get_distance_time(orders[0], orders[1:4])
    assert len(nearby_orders) == len(distances) == len(times)

def _test_batching(orders):
    maps = gmaps.GMaps()
    nearby_orders, distances, times = maps.get_distance_time(orders[0], orders[1:], chunk_size=2)
    assert len(nearby_orders) == len(distances) == len(times) == 4

def test_singleton(orders):
    a_maps = gmaps.GMaps()
    b_maps = gmaps.GMaps()
    assert a_maps == b_maps

def test_get_distance_btw(orders):
    maps = gmaps.GMaps()
    leg = maps.get_distance_between(orders[0], orders[1])

    assert leg.source == orders[0]
    assert leg.destination == orders[1]
