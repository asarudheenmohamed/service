"""Endpoint to get optimum routing."""
import datetime
import logging

from django.db.models import Q

import pyproj as proj
from app.core.models import CoreStore, SalesFlatOrder
from app.driver.models.driver_order import DriverOrder
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# Get an instance of a logger
logger = logging.getLogger(__name__)


def manhattan_distance(position_1, position_2):
    """Computes the Manhattan distance between two points"""
    return (abs(position_1[0] - position_2[0]) +
            abs(position_1[1] - position_2[1]))


class Vehicle():
    """Stores the property of a driver"""

    def __init__(self):
        """Initializes the vehicle properties"""
        # 20 items
        self._capacity = 30
        # Travel speed: 20km/h to convert in m/min
        self._speed = 30 * 60 / 3.6

    @property
    def capacity(self):
        """Gets vehicle capacity"""
        return self._capacity

    @property
    def speed(self):
        """Gets the average travel speed of a vehicle"""
        return self._speed


class RoutingData:

    # time for the rider to scan and take in the app.
    INITIAL_BUFFER_TIME = 0

    def __init__(self, store_id):
        """
        :param store_id: Store id for which we collect all the processing orders.
        """
        self.store_id = store_id
        today = format(datetime.date.today(), '%Y-%m-%d')
        self.orders = self.fetch_orders()
        # +1 to counter the depot location also
        self.cache = {index + 1: order for index,
                      order in enumerate(self.orders)}
        self.vehicle = Vehicle()
        self.num_vehicles = 20

        self.depot = 0
        # location for all orders.
        self.time_windows, self.time_per_order, self.locations = self.prepare_location_data()
        logger.info(self.time_windows)
        logger.info(self.time_per_order)
        logger.info(self.locations)
        # Item counts for all orders
        self.demands = self.generate_demands()
        # time window for all orders

    @property
    def num_locations(self):
        """Gets number of locations"""
        return len(self.locations)

    def fetch_orders(self):
        """Fetch the non assign orders based on store_id.

    Returns:
         sale order object
        """
        today = format(datetime.date.today(), '%Y-%m-%d')

        order = SalesFlatOrder.objects.filter(
            store_id=self.store_id,
            status='processing',
            sale_date__gte=today,
            driver_number__isnull=True).prefetch_related('items', 'shipping_address')

        return order

    def prepare_location_data(self):
        """Get all lat and lng and convert to cartesian
        coordinates

        :return:
            A list of (x, y)
        """

        time_windows = [(0, 0)]
        time_per_order = [0]
        locations = []

        # map to hold addresses, so that we can set the times to zero for
        # same addresses.
        address_map = {}
        for order in self.orders:
            shipping_address = order.shipping_address.all().filter(
                address_type='shipping').first()

            locations.append((shipping_address.o_latitude,
                              shipping_address.o_longitude))
            # time per order
            if not address_map.get(shipping_address.customer_address_id, None):
                # Flat 8 mins.
                time_per_order.append(8)
                address_map[shipping_address.customer_address_id] = True
            else:
                # same location then 0 buffer.
                time_per_order.append(0)

            # this is the min time to deliver the order, scanning + eta
            min_time = shipping_address.eta + self.INITIAL_BUFFER_TIME
            # Time windows: if the order cannot be serviced, then we put in mintime itself
            # so it can get prioritized.
            time_remaining = min_time + \
                10 if order.remaining_time < min_time else order.remaining_time
            time_windows.append(
                (self.INITIAL_BUFFER_TIME, int(time_remaining)))

        # setup your projections
        # assuming you're using WGS84 geographic
        crs_wgs = proj.Proj(init='epsg:4326')
        # use a locally appropriate projected CRS
        crs_bng = proj.Proj(init='epsg:27700')

        locations = [proj.transform(crs_wgs, crs_bng, location[0], location[1])
                     for location in locations]

        store_lat_and_lng = CoreStore.objects.filter(
            store_id=self.store_id).values(
            'location__longandlatis__longitude',
            'location__longandlatis__latitude').first()

        depot = proj.transform(crs_wgs, crs_bng,
                               store_lat_and_lng['location__longandlatis__latitude'],
                               store_lat_and_lng['location__longandlatis__longitude'])
        locations.insert(0, depot)

        return time_windows, time_per_order, locations

    def generate_demands(self):
        """Count of all order items."""
        demands = [0]
        for order in self.orders:
            demands.append(len(order.items.all()))
        return demands


class CreateDistanceEvaluator(object):
    """Creates callback to return distance between points."""

    def __init__(self, data):
        """Initializes the distance matrix."""
        self._distances = {}

        # precompute distance between location to have distance callback in O(1)
        for from_node in xrange(data.num_locations):
            self._distances[from_node] = {}
            for to_node in xrange(data.num_locations):
                if from_node == to_node:
                    self._distances[from_node][to_node] = 0
                else:
                    self._distances[from_node][to_node] = (
                        manhattan_distance(
                            data.locations[from_node],
                            data.locations[to_node]))

    def distance_evaluator(self, from_node, to_node):
        """Returns the manhattan distance between the two nodes"""
        return self._distances[from_node][to_node]


class CreateDemandEvaluator(object):
    """Creates callback to get demands at each location."""

    def __init__(self, data):
        """Initializes the demand array."""
        self._demands = data.demands

    def demand_evaluator(self, from_node, to_node):
        """Returns the demand of the current node"""
        del to_node
        return self._demands[from_node]


class CreateTimeEvaluator(object):
    """Creates callback to get total times between locations."""

    @staticmethod
    def service_time(data, from_node, to_node):
        """Gets the service time for the specified location."""
        # return data.demands[node] * data.time_per_demand_unit
        return data.time_per_order[to_node]

    @staticmethod
    def travel_time(data, from_node, to_node):
        """Gets the travel times between two locations."""
        if from_node == to_node:
            travel_time = 0
        else:
            travel_time = manhattan_distance(
                data.locations[from_node],
                data.locations[to_node]) / data.vehicle.speed
        return travel_time

    def __init__(self, data):
        """Initializes the total time matrix."""
        self._total_time = {}
        # precompute total time to have time callback in O(1)
        for from_node in xrange(data.num_locations):
            self._total_time[from_node] = {}
            for to_node in xrange(data.num_locations):
                if from_node == to_node:
                    self._total_time[from_node][to_node] = 0
                else:
                    self._total_time[from_node][to_node] = int(
                        self.service_time(data, from_node, to_node) +
                        self.travel_time(data, from_node, to_node))

    def time_evaluator(self, from_node, to_node):
        """Returns the total time between the two nodes"""
        return self._total_time[from_node][to_node]


def add_capacity_constraints(routing, data, demand_evaluator):
    """Adds capacity constraint"""
    capacity = "Capacity"
    routing.AddDimension(
        demand_evaluator,
        0,  # null capacity slack
        data.vehicle.capacity,  # vehicle maximum capacity
        True,  # start cumul to zero
        capacity)


def add_time_window_constraints(routing, data, time_evaluator):
    """Add Global Span constraint"""
    time = "Time"
    horizon = 120
    routing.AddDimension(
        time_evaluator,
        3,  # allow waiting time
        horizon,  # maximum time per vehicle
        False,  # don't force start cumul to zero since we are giving TW to start nodes
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    for location_idx, time_window in enumerate(data.time_windows):
        if location_idx == 0:
            continue
        index = routing.NodeToIndex(location_idx)
        logger.info(time_window)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
    for vehicle_id in xrange(data.num_vehicles):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data.time_windows[0][0], data.time_windows[0][1])
        routing.AddToAssignment(time_dimension.SlackVar(index))


class ConsolePrinter():
    """Print solution to console"""

    def __init__(self, data, routing, assignment):
        """Initializes the printer"""
        self._data = data
        self._routing = routing
        self._assignment = assignment

    @property
    def data(self):
        """Gets problem data"""
        return self._data

    @property
    def routing(self):
        """Gets routing model"""
        return self._routing

    @property
    def assignment(self):
        """Gets routing model"""
        return self._assignment

    def printer(self):
        """Prints assignment on console"""
        # Inspect solution.
        capacity_dimension = self.routing.GetDimensionOrDie('Capacity')
        time_dimension = self.routing.GetDimensionOrDie('Time')
        total_dist = 0
        total_time = 0
        for vehicle_id in xrange(self.data.num_vehicles):
            index = self.routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {0}:\n'.format(vehicle_id)
            route_dist = 0
            while not self.routing.IsEnd(index):
                node_index = self.routing.IndexToNode(index)
                next_node_index = self.routing.IndexToNode(
                    self.assignment.Value(self.routing.NextVar(index)))
                route_dist += manhattan_distance(
                    self.data.locations[node_index],
                    self.data.locations[next_node_index])

                load_var = capacity_dimension.CumulVar(index)
                route_load = self.assignment.Value(load_var)

                time_var = time_dimension.CumulVar(index)
                time_min = self.assignment.Min(time_var)
                time_max = self.assignment.Max(time_var)

                slack_var = time_dimension.SlackVar(index)
                slack_min = self.assignment.Min(slack_var)
                slack_max = self.assignment.Max(slack_var)

                plan_output += ' {0} Load({1}) Time({2},{3}) Slack({4},{5}) ->'.format(
                    node_index,
                    route_load,
                    time_min, time_max,
                    slack_min, slack_max)
                index = self.assignment.Value(self.routing.NextVar(index))

            node_index = self.routing.IndexToNode(index)
            load_var = capacity_dimension.CumulVar(index)
            route_load = self.assignment.Value(load_var)
            time_var = time_dimension.CumulVar(index)
            route_time = self.assignment.Value(time_var)
            time_min = self.assignment.Min(time_var)
            time_max = self.assignment.Max(time_var)
            total_dist += route_dist
            total_time += route_time
            plan_output += ' {0} Load({1}) Time({2},{3})\n'.format(
                node_index, route_load, time_min, time_max)
            plan_output += 'Distance of the route: {0}m\n'.format(route_dist)
            plan_output += 'Load of the route: {0}\n'.format(route_load)
            plan_output += 'Time of the route: {0}min\n'.format(route_time)
            logger.info(plan_output)
        logger.info('Total Distance of all routes: {0}m'.format(total_dist))
        logger.info('Total Time of all routes: {0}min'.format(total_time))


class RoutingController():

    def format_output(self, routing, data, assignment):
        """Format the routings into dicts."""
        routes = []
        time_dimension = routing.GetDimensionOrDie('Time')
        for vehicle_id in xrange(data.num_vehicles):
            # Depot
            index = routing.Start(vehicle_id)

            route = {'orders': [], 'km': 0}
            while not routing.IsEnd(index):
                # Get the next index.
                index = assignment.Value(routing.NextVar(index))

                if not data.cache.get(index, None):
                    continue

                node_index = routing.IndexToNode(index)
                next_node_index = routing.IndexToNode(
                    assignment.Value(routing.NextVar(index)))

                route['km'] += manhattan_distance(
                    data.locations[node_index],
                    data.locations[next_node_index])
                route['orders'].append(data.cache[index].increment_id)

            # Driver was not used, so skip it.
            if not route['orders']:
                continue

            # Inject time finally.
            time_var = time_dimension.CumulVar(index)
            route['time'] = assignment.Value(time_var)
            route['km'] = round(route['km'] / 1000, 2)
            routes.append(route)

        return routes

    def generate_optimal_routes(self, store_id):
        """Entry point of the program

        :return
            A list of dicts containing{orders, km, time}
        """
        # Instantiate the data problem.
        data = RoutingData(store_id)

        # Create Routing Model
        routing = pywrapcp.RoutingModel(
            data.num_locations, data.num_vehicles, data.depot)

        # Define weight of each edge
        distance_evaluator = CreateDistanceEvaluator(data).distance_evaluator
        logger.info(CreateDistanceEvaluator(data)._distances)
        routing.SetArcCostEvaluatorOfAllVehicles(distance_evaluator)

        # Add Capacity constraint
        demand_evaluator = CreateDemandEvaluator(data).demand_evaluator
        add_capacity_constraints(routing, data, demand_evaluator)

        # Add Time Window constraint
        time_evaluator = CreateTimeEvaluator(data).time_evaluator
        add_time_window_constraints(routing, data, time_evaluator)

        # Setting first solution heuristic (cheapest addition).
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        logger.info("status was {}".format(routing.status()))
        # printer = ConsolePrinter(data, routing, assignment)

        return self.format_output(routing, data, assignment)
