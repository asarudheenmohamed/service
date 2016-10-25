# 0,1,15,6
# 2.0.7.3
# 9, 6,0,12
# 10,4,8,0
# 21


import itertools
from scipy.spatial import distance

class TSP:
    def __init__(self):
        self.cache = {}

    def subsets(self, data):
        for index in range(1, len(data)+1):
            for subset in itertools.combinations(data, index):
                yield subset

    def _get_min_distance(self, start_order, dest_order, waypoints):
        min_distance, parent = float('inf'), None
        for i, waypoint_order in enumerate(waypoints):
            curr_distance = self.get_distance(waypoint_order, dest_order)
            print ("distance from {} -> {} is {}".format(
                    waypoint_order, dest_order, self.get_distance(waypoint_order, dest_order) ))

            remaining_waypoints = tuple(waypoints[:i] + waypoints[i+1:])
            w_distance, _ = self.cache[(waypoint_order, remaining_waypoints)]
            curr_distance += w_distance

            if curr_distance < min_distance:
                min_distance = curr_distance
                parent = waypoint_order

        return min_distance, parent

    def get_distance(self, from_order, to_order):
        return distance.cityblock((from_order.x, from_order.y, from_order.z),
                           (to_order.x, to_order.y, to_order.z))

    def distance(self, start_order, other_orders):

        for waypoints_combinations in self.subsets(other_orders):
            for dest_order in other_orders:
                if (dest_order, ()) not in self.cache:
                    self.cache[(dest_order, ())] = \
                    (self.get_distance(start_order, dest_order), start_order)

                if dest_order in waypoints_combinations:
                    continue

                self.cache[(dest_order, waypoints_combinations)] = \
                        self._get_min_distance(
                            start_order,
                            dest_order,
                            waypoints_combinations)

        self.cache[(start_order, other_orders)] = \
            self._get_min_distance(start_order, dest_order, other_orders)
        print ("((((((((((((((((((((((((")
        print (self.cache[(start_order, other_orders)])



        _, parent = self.cache[(start_order, other_orders)]
        route = [start_order]

        while other_orders:
            route.append(parent)
            index = other_orders.index(parent)
            other_orders = tuple(other_orders[:index] + other_orders[index+1:])
            _, parent = self.cache[(parent, other_orders)]

        route.reverse()
        return route
