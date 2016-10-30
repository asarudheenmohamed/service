from django.db import models
import abc
from django.template.defaultfilters import default
from enum import Enum
class InvalidLeg(Exception):
    pass

class Leg(models.Model):

    leg_id = models.AutoField(primary_key=True)
    distance = models.FloatField()
    duration = models.IntegerField()
    source = models.ForeignKey("order", on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey("order", on_delete=models.CASCADE, related_name='destination')

class RouteType(Enum):
    Route = 0
    PseudoRoute = 1

class Route(models.Model):
    total_distance = models.FloatField(default=0)
    total_duration = models.FloatField(default=0)

    @classmethod
    def from_psuedo_route(cls, psuedo_route, gapi):
        legs = gapi.get_route(psuedo_route)

        route = cls.objects.create(source=legs[0].source)

        for i, leg in enumerate(legs):
            if route.can_add(leg):
                route.add_leg(leg)
            else:
                break

        # reset the assigned flag
        if i != len(legs) - 1:
            for leg in legs[i:]:
                leg.destination.unassign_route()

        route.commit()

        return route

    def __init__(self, *args, source=None, route_type=RouteType.Route, **kwargs):
        super().__init__(*args, **kwargs)
        self.route_type = route_type
        self.points = []

        # Source
        if source:
            self._add_order(source)

    def can_add(self, leg):
        """
        Duration in seconds
        """
        if len(self.points) == 1:
            return True

        return self.total_duration + leg.duration + self.point_buffer <= self.max_capacity

    @property
    def max_capacity(self):
        if self.route_type == RouteType.Route:
            return  90 * 60

        return  180 * 60

    @property
    def point_buffer(self):
        return  10 * 60

    @property
    def latest_stop(self):
        return self.points[-1]

    def add_leg(self, leg):
        if self.latest_stop.order_id != leg.source.order_id:
#             print (self.latest_stop.__dict__, leg.source.__dict__)
            raise InvalidLeg

        self._add_order(leg.destination)

        self.total_distance += leg.distance
        self.total_duration += leg.duration + self.point_buffer

    def _add_order(self, order):
        self.points.append(order)
        order.assign_route(self)

    def commit(self):
        for i, order in enumerate(self.points):
            order.route_order = i
            order.save()
            self.orders.add(order)
