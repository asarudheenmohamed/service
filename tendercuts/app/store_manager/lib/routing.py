"""Endpoint to get optimum routing."""
import logging

import pyproj as proj
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from app.core.models import SalesFlatOrder

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
        self._capacity = 20
        # Travel speed: 5km/h to convert in m/min
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
    def __init__(self, store_id):
        """
        :param store_id: Store id for which we collect all the processing orders.
        """
        self.orders = SalesFlatOrder.objects.filter(store_id=store_id, status='processing')[:11]
        self.orders = self.orders.prefetch_related('items', 'shipping_address')

        # +1 to counter the depot location also
        self.cache = {index + 1: order for index, order in enumerate(self.orders)}
        self.vehicle = Vehicle()
        self.num_vehicles = 8

        # location for all orders.
        self.locations = self.prepare_locations()
        self.depot = 0
        # Item counts for all orders
        self.demands = self.generate_demands()
        # time window for all orders
        self.time_windows = self.generate_times()

    @property
    def num_locations(self):
        """Gets number of locations"""
        return len(self.locations)

    @property
    def time_per_demand_unit(self):
        """Gets the time (in min) to load a demand"""
        return 8  # 5 minutes/unit

    def prepare_locations(self):
        """Get all lat and lng and convert to cartesian
        coordinates

        :return:
            A list of (x, y)
        """
        locations = [(
            order.shipping_address.all()[0].o_latitude,
            order.shipping_address.all()[0].o_longitude)
            for order in self.orders]

        locations = [
            (12.989885, 80.221038),
            (12.972565, 80.263893),
            (12.98757, 80.251768),
            (12.91676, 80.263095),
            (12.989989, 80.24147),
            (12.980484, 80.271442),
            (12.97396, 80.233544),
            (12.913834, 80.23268),
            (12.971158, 80.225461),
            (12.999628, 80.264873),
            (12.998304, 80.268419),
        ]
        # setup your projections
        crs_wgs = proj.Proj(init='epsg:4326')  # assuming you're using WGS84 geographic
        crs_bng = proj.Proj(init='epsg:27700')  # use a locally appropriate projected CRS

        locations = [proj.transform(crs_wgs, crs_bng, location[0], location[1])
                     for location in locations]

        depot = proj.transform(crs_wgs, crs_bng, '12.928171', '80.235877')
        locations.insert(0, depot)

        return locations

    def generate_demands(self):
        """Count of all order items."""
        demands = [0]
        for order in self.orders:
            demands.append(len(order.items.all()))
        return demands

    def generate_times(self):
        """Get the time remaining for all orders.

        Note: If negative time is remaining, then the logic will
        break so we keep a steady timing of 35 mins for orders.
        """
        time_windows = [(0, 0)]
        for order in self.orders:
            time_remaining = 35 if order.remaining_time < 0 else order.remaining_time
            time_windows.append((0, time_remaining))

        return time_windows


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
    def service_time(data, node):
        """Gets the service time for the specified location."""
        # return data.demands[node] * data.time_per_demand_unit
        return data.time_per_demand_unit

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
                        self.service_time(data, from_node) +
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
        5,  # allow waiting time
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
        time_dimension.CumulVar(index).SetRange(data.time_windows[0][0], data.time_windows[0][1])
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
            plan_output += ' {0} Load({1}) Time({2},{3})\n'.format(node_index, route_load, time_min, time_max)
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
        routing = pywrapcp.RoutingModel(data.num_locations, data.num_vehicles, data.depot)

        # Define weight of each edge
        distance_evaluator = CreateDistanceEvaluator(data).distance_evaluator
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
            routing_enums_pb2.FirstSolutionStrategy.SAVINGS)

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        # printer = ConsolePrinter(data, routing, assignment)

        return self.format_output(routing, data, assignment)
