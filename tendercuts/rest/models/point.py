from django.db import models
import math

class GeoCoordinate(object):

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
        return str(self.lat) + ',' + str(self.long)


class GeoCoordinateField(models.CharField):
    description = "A latitude,longitude pair"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        kwargs['blank'] = False
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]

        return name, path, args, kwargs

    def parse_coord(self, value):
        print (value)
        args = [float(value.split(',')[0]), float(value.split(',')[1])]

        if len(args) != 2 and value is not None:
            raise ValueError("Invalid input for a GeoCoordinate instance")

        return GeoCoordinate(*args)

    def from_db_value(self, value, expression, connection, context):
        if value in (None, ''):
            return value
        return self.parse_coord(value)

    def to_python(self, value):
        if isinstance(value, GeoCoordinate):
            return value

        if value in (None, ''):
            return value

        return self.parse_coord(value)

    def get_prep_value(self, value):
        return ','.join([str(value.lat),str(value.long)])

class AbstractMapPoint(models.Model):
    location = GeoCoordinateField()
    class Meta:
        app_label="rest"
        abstract = True


class Order(AbstractMapPoint):
    order_id = models.CharField(max_length=50, primary_key=True)
    route = models.ForeignKey('route', null=True, related_name='orders')

    @classmethod
    def from_dict(cls, data):
        geo = GeoCoordinate(data['lat'], data['long'])
        return cls.objects.create(order_id=data['id'], location=geo)

    @property
    def is_assigned(self):
        return self.route is not None

    def assign_route(self, route):
#         self.route = route
        route.orders.add(self)

    def unassign_route(self):
#         self.route = None
        self.route.orders.remove(self)