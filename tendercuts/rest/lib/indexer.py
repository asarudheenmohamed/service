import scipy.spatial
import logging
import numpy as np
from heapq import heappop, heappush

class OrderTree(scipy.spatial.KDTree):
    def __init__(self, orders, leafsize=10):
        self.orders = orders
        data = self._extract_coords(self.orders)
        print (data)
        super().__init__(data, leafsize)

        # Ugly hack till we have an own implementation of KD-Tree
        func_name = "_KDTree__query"
        setattr(self, func_name, self.__query)

    def _extract_coords(self, orders):
        return [(order.location.x, order.location.y, order.location.z) for order in orders]

    def __query(self, x, k=1, eps=0, p=2, distance_upper_bound=np.inf):

        side_distances = np.maximum(0,np.maximum(x-self.maxes,self.mins-x))
        if p != np.inf:
            side_distances **= p
            min_distance = np.sum(side_distances)
        else:
            min_distance = np.amax(side_distances)

        # priority queue for chasing nodes
        # entries are:
        #  minimum distance between the cell and the target
        #  distances between the nearest side of the cell and the target
        #  the head node of the cell
        q = [(min_distance,
              tuple(side_distances),
              self.tree)]
        # priority queue for the nearest neighbors
        # furthest known neighbor first
        # entries are (-distance**p, i)
        neighbors = []

        if eps == 0:
            epsfac = 1
        elif p == np.inf:
            epsfac = 1/(1+eps)
        else:
            epsfac = 1/(1+eps)**p

        if p != np.inf and distance_upper_bound != np.inf:
            distance_upper_bound = distance_upper_bound**p

        while q:
            min_distance, side_distances, node = heappop(q)
            if isinstance(node, scipy.spatial.KDTree.leafnode):
                # brute-force

                data = self.data[node.idx]
                ds = scipy.spatial.minkowski_distance_p(data,x[np.newaxis,:],p)
                for i in range(len(ds)):
                    if ds[i] < distance_upper_bound:
                        if len(neighbors) == k:
                            heappop(neighbors)

                        order = self.orders[node.idx[i]]
                        if not order.is_assigned:
                            heappush(neighbors, (-ds[i], node.idx[i]))
                        if len(neighbors) == k:
                            distance_upper_bound = -neighbors[0][0]
            else:
                # we don't push cells that are too far onto the queue at all,
                # but since the distance_upper_bound decreases, we might get
                # here even if the cell's too far
                if min_distance > distance_upper_bound*epsfac:
                    # since this is the nearest cell, we're done, bail out
                    break
                # compute minimum distances to the children and push them on
                if x[node.split_dim] < node.split:
                    near, far = node.less, node.greater
                else:
                    near, far = node.greater, node.less

                # near child is at the same distance as the current node
                heappush(q,(min_distance, side_distances, near))

                # far child is further by an amount depending only
                # on the split value
                sd = list(side_distances)
                if p == np.inf:
                    min_distance = max(min_distance, abs(node.split-x[node.split_dim]))
                elif p == 1:
                    sd[node.split_dim] = np.abs(node.split-x[node.split_dim])
                    min_distance = min_distance - side_distances[node.split_dim] + sd[node.split_dim]
                else:
                    sd[node.split_dim] = np.abs(node.split-x[node.split_dim])**p
                    min_distance = min_distance - side_distances[node.split_dim] + sd[node.split_dim]

                # far child might be too far, if so, don't bother pushing it
                if min_distance <= distance_upper_bound*epsfac:
                    heappush(q,(min_distance, tuple(sd), far))

        if p == np.inf:
            return sorted([(-d,i) for (d,i) in neighbors])
        else:
            return sorted([((-d)**(1./p),i) for (d,i) in neighbors])

class LocationIndexer:
    def __init__(self, orders, log=None):
        """
        """
        self._orders = orders
#         self._coordinates = self._extract_coords()
#         self._tree = scipy.spatial.KDTree(self._coordinates, leafsize=2)
        self._tree = OrderTree(self._orders, leafsize=2)

#         self._gmaps_api = gmaps_api
        self.log = log or logging.getLogger()

    def _extract_coords(self):
        return [(order.x, order.y, order.z) for order in self._orders]

    def get_nearby_orders(self, target_order,  radius=100, neighbours=30, exclude_assigned=True):
        neighbours += 1

        input_coords = (target_order.location.x, target_order.location.y, target_order.location.z)
        self.log.debug ("Computing nearby cordinates for order {}".format(
                target_order))
        distances, indexes = self._tree.query(input_coords, k=neighbours, p=1)#, distance_upper_bound=radius)

        if type(distances) is not np.ndarray:
            return []

        distances, orders = self._filter_orders(target_order, distances, indexes)

        return distances, orders

    def _filter_orders(self, target_order, distances, indexes, exclude_assigned=True):

        f_orders, f_distances = [], []
        for index, distance in zip(indexes, distances):
            if distance == float('inf'):
                continue

            order = self._orders[index]
            # Remove the same order!!
            if order is target_order:
                continue

#             # We dont give a damn about the order that have already been assigned
            if exclude_assigned and order.is_assigned:
                continue

            f_orders.append(order)
            f_distances.append(distance)

        return f_distances, f_orders