import logging
from datetime import datetime

import googlemaps
from django.conf import settings

from rest.models import Leg


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


# class GMaps(metaclass=Singleton):
class GMaps():
    __metaclass__ = Singleton

    def __init__(self, is_premium=False, log=None):
        self._api = googlemaps.Client(
            key=settings.GOOGLE_MAP_DISTANCE_API['KEY'])
        self.is_premium = is_premium
        self.log = logging.getLogger()

    def get_distance_time(self, target_order, nearby_orders, chunk_size=None):
        self.log.debug("Computing distance for {} orders from current order {}".format(
            len(nearby_orders), target_order
        ))

        def chunks(arr, chunk_size):
            for i in range(0, len(arr), chunk_size):
                self.log.debug(
                    "Batching orders {} to {}".format(
                        i, i + chunk_size))
                yield arr[i:i + chunk_size]

        source = (target_order.lat, target_order.long)
        destinations = [(order.lat, order.long) for order in nearby_orders]

        if not chunk_size:
            chunk_size = 625 if self.is_premium else 25

        now = datetime.now()
        distances, times = [], []
        for destination_set in chunks(destinations, chunk_size):
            # Need to move it
            response = self._api.distance_matrix(
                source,
                destination_set,
                departure_time=now,
                mode="driving")

            data = response['rows'][0]['elements']
            for distance_data in data:
                distances.append(distance_data['distance']['value'])
                times.append(distance_data['duration_in_traffic']['value'])

        return nearby_orders, distances, times

    def get_distance_between(self, source, destination):
        now = datetime.now()

        source_coords = (source.lat, source.long)
        destination_coords = (destination.lat, destination.long)

        response = self._api.distance_matrix(
            source_coords,
            destination_coords,
            departure_time=now,
            mode="driving")

        # only one will exists
        data = response['rows'][0]['elements'][0]
        return model.Leg.from_gmaps_data(source, destination, data)

    def get_route(self, route):
        coords = [(order.location.lat, order.location.long)
                  for order in route.points]
        source = coords[0]
        destination = coords[-1]
        waypoints = coords[1:-1]

        self.log.debug("Generating legs from Route {} containing {} orders".format(
            route, len(coords)))

        res = self._api.directions(origin=source,
                                   destination=destination,
                                   waypoints=waypoints)

        legs = []
        for source, destination, data in zip(
                route.points[:-1], route.points[1:], res[0]['legs']):
            duration = data['duration']['value']
            distance = data['distance']['value']
            legs.append(Leg(source=source, destination=destination,
                            duration=duration, distance=distance))

        self.log.debug(
            "Generated {} legs for {} route".format(
                len(legs), route))

        return legs
