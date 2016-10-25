import math

class MapPoint(object):
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

        self.x, self.y,  self.z = self._generate_cartesian_coords()

    def _generate_cartesian_coords(self):
        lat, long = float(self.lat), float(self.long)

        lat, long = math.radians(lat), math.radians(long)
        R = 6373  # radius of earth

        x = R * math.cos(lat) * math.cos(long)
        y = R * math.cos(lat) * math.sin(long)
        z = R * math.sin(lat)

        return x, y, z

    def __repr__(self):
        return "lat: {}, long: {}".format(self.lat, self.long)


class Order(MapPoint):
    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['lat'], data['long'])

    def __init__(self, id, lat, long):
        super().__init__(lat, long)
        self.id = id
        self._route = None

    @property
    def is_assigned(self):
        return self._route is not None

    def assign_route(self, route):
        self._route = route

    def unassign_route(self):
        self._route = None

class DistributionCenter(MapPoint):
    def __init__(self, id, lat, long):
        super().__init__(lat, long)
        self.id = id
