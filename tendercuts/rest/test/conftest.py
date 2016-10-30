from datetime import datetime

import pytest
import googlemaps
import logging

from rest.lib.indexer import LocationIndexer
from rest.models.point import Order


@pytest.fixture
def orders():
    orders = []
    coords = [
            (12.92908, 77.62187900000004),
            (12.930011939588985, 77.62474358081818),
            (12.931444516664055, 77.62464702129364),
            (12.931323157570429, 77.62162902432863),
#             (12.931392232973792, 77.62230813503265),
            (12.934325331065297, 77.62361705303192),
            (12.932113746931863, 77.62368679046631),
            (12.924192664232187, 77.61876225471497),
            (12.925682788093471, 77.61667549610138),
            (12.923371785183274, 77.61576890945435),
            (12.921745704705058, 77.62393355369568),
            (12.92409332232521, 77.62592375278473),
            (12.923936466602155, 77.63002753257751),
            (12.933274438921474, 77.61231422424316),
            (12.932667951888742, 77.6069712638855),
            (12.930304729732805, 77.60546922683716),
            (12.936787852031962, 77.6063060760498),
            (12.935261196461985, 77.60431051254272),
            (12.942183354375915, 77.61360168457031),
            (12.94226700465603, 77.61164903640747),
            (12.944044566473055, 77.60701417922974),
            (12.94458828873272, 77.61664867401123),
            (12.940928596806609, 77.62276411056519),
            (12.945529343687165, 77.62130498886108),
            (12.946512219512973, 77.62368679046631),
            (12.942957118395979, 77.62913703918457),
            (12.940426692010892, 77.62900829315186),
        ]

    for order_id, cord in enumerate(coords):
        model = Order.from_dict({'id': str(order_id),
                              'lat': cord[0],
                              'long': cord[1]})
        orders.append(model)

    logging.debug("Generating test data for {} orders".format(len(orders)))

    return orders


@pytest.fixture
def indexer(orders):
    indexer = LocationIndexer(orders)
    return indexer


@pytest.fixture
def distance_between():
    api = googlemaps.Client(key='AIzaSyCQK2O4AMogjO323B-6btf9f2krVWST3bU')

    def wrapper(source, destination):
        now = datetime.now()
        response = api.distance_matrix(
                    source,
                    destination,
                    departure_time=now,
                    mode="driving")

        data = response['rows'][0]['elements'][0]

        return data['distance']['value'], data['duration_in_traffic']['value']
    return wrapper