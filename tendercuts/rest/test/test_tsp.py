from rest.lib import tsp
import collections
from scipy.spatial import distance

def test_tsp1(orders):

#     distance = [[0, 1, 15, 6],
#                [2, 0, 7, 3],
#                [9, 6, 0, 12],
#                [10, 4, 8, 0]]

    route_tsp = tsp.TSP()
    route = route_tsp.distance(orders[0], tuple(orders[1:5]))


    def get_distance(from_order, to_order):
        return distance.cityblock((from_order.x, from_order.y, from_order.z),
                           (to_order.x, to_order.y, to_order.z))

#     distance_t = collections.defaultdict(dict)
    distance_t = [[0] * len(orders[:5]) for i in  range(len(orders[:5]))]
    print (distance_t)


    for i, s_order in enumerate(orders[:5]):
        for j, t_order in enumerate(orders[:5]):
            if s_order is t_order:
                continue
            print (i, j)

            distance_t[i][j] = "%.2f" % get_distance(s_order, t_order)


    print (distance_t)
    assert route == [1, 3, 2, 0]

