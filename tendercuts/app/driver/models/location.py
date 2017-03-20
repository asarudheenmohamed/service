from __future__ import unicode_literals


import math

from app.core import models as core_model
from django.contrib.auth.models import User
from django.db import models


class GeoCoordinate(object):

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

        self.x, self.y, self.z = self._generate_cartesian_coords()

    def _generate_cartesian_coords(self):
        lat, lng = float(self.lat), float(self.lng)

        lat, lng = math.radians(lat), math.radians(lng)
        R = 6373  # radius of earth

        x = R * math.cos(lat) * math.cos(lng)
        y = R * math.cos(lat) * math.sin(lng)
        z = R * math.sin(lat)

        return x, y, z

    def __repr__(self):
        return str(self.lat) + ',' + str(self.long)


class GeoCoordinateField(models.CharField):
    description = "A latitude,longitude pair"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        kwargs['blank'] = False
        super(GeoCoordinateField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(GeoCoordinateField, self).deconstruct()
        del kwargs["max_length"]

        return name, path, args, kwargs

    def parse_coord(self, value):
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
        value = self.parse_coord(value)
        return ','.join([str(value.lat),str(value.lng)])


class DriverLocation(models.Model):
    row_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now=True)
    location = GeoCoordinateField()

    @property
    def driver(self):
        driver = core_model.DriverManagement.objects.filter(phone=self.user.username)
        return driver[0]

