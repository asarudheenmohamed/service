from datetime import datetime
import logging
import time

import numpy
import scipy.spatial

from rest.models import Route, Leg, RouteType
from .indexer import LocationIndexer
from .gmaps import GMaps

logging.getLogger().setLevel(logging.DEBUG)

class Engine:
    def __init__(self, dist, log=None):
#         self.gmaps_api = gmaps_api
        self.distribution_center = dist
        self.log = logging.getLogger()
        self._gapi = GMaps()

    def generate_route(self, orders ,indexer):

        route = Route.objects.create(route_type=RouteType.PseudoRoute)
        route.points.append(self.distribution_center)
        route.orders.add(self.distribution_center)
#         self.distribution_center.route_order = 0
#         route._counter += 1

        neighbours = 6 ## Hack!! Needs to derived from route

        distances, nearby_orders = indexer.get_nearby_orders(
            route.latest_stop,
            neighbours=neighbours)

        # Run till all orders have been filled or till the route's capacity is
        # done.
        while nearby_orders:
            time = distances[0] * 60
            leg = Leg(source=route.latest_stop, destination=nearby_orders[0], duration=time, distance=distances[0])
            if not route.can_add(leg):
                break

            route.add_leg(leg)
            distances, nearby_orders = indexer.get_nearby_orders(
                route.latest_stop,
                neighbours=neighbours)

        return route

    def generate_routes(self, orders):
        self._location_indexer = LocationIndexer(orders)

        routes = []
        all_done = False
        while not all_done:
            start_time = time.time()
            pseudo_route = self.generate_route(orders, self._location_indexer)
            end_time = time.time()
            print ("Time take to compute a pseudo route {}".format(end_time - start_time))
#             import pdb
#             pdb.set_trace()

            start_time = time.time()
            route = Route.from_psuedo_route(pseudo_route, self._gapi)
            end_time = time.time()
#             print ("Time take to compute a route {}".format(end_time - start_time))
            routes.append(route)
            all_done = [order.is_assigned for order in orders]
            all_done = all(all_done)

        return routes
