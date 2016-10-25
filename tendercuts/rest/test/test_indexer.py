import pytest
import functools
import math


def test_diff_bt_indexer_gmaps(orders, indexer, distance_between):
    first_order, second_order = orders[1], orders[2]

    distances, orders = indexer.get_nearby_orders(first_order, neighbours=2)
    i_distance = distances[0]

    source = (first_order.lat, first_order.long)
    destination = (orders[0].lat, orders[0].long)
    g_distance, time = distance_between(source, destination)

    g_distance /= 1000
    avg = (g_distance + i_distance) / 2
    percent_diff = abs(g_distance - i_distance) / avg
    percent_diff *= 100
    print (g_distance, i_distance)

    assert percent_diff < 40

def test_neighbours(orders, indexer):
    first_order, second_order = orders[0], orders[1]
    distances, orders = indexer.get_nearby_orders(first_order, neighbours=2)
    assert len(orders) == 2

def test_radius(orders, indexer):
    first_order, second_order = orders[0], orders[1]
    distances, orders = indexer.get_nearby_orders(first_order, neighbours=2, radius=8)
    assert distances[0] < 8

def test_not_the_same_order(orders, indexer):
    """
    Make sure we don't end up getting the same order again
    """
    first_order, second_order = orders[0], orders[1]
    distances, norders = indexer.get_nearby_orders(first_order, neighbours=2, radius=8)
    print (orders)
    assert norders[ 0] != first_order

def test_assigned(orders, indexer):
    """
    Assert the already assigned orders are not returned
    """
    first_order, second_order = orders[0], orders[1]

    for order in orders[1:]:
        order.assign_route(1)
    distances, orders = indexer.get_nearby_orders(first_order, neighbours=2, radius=8)
    assert not orders
