from django.db import models
import abc

class InvalidLeg(Exception):
    pass

class Leg(models.Model):

    leg_id = models.AutoField(primary_key=True)
    distance = models.FloatField()
    duration = models.IntegerField()
    source = models.ForeignKey("order", on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey("order", on_delete=models.CASCADE, related_name='destination')


class Route(models.Model):
    total_distance = models.FloatField()
    total_duration = models.FloatField()

    def can_add(self, order_duration):
        """
        Duration in seconds
        """
        if len(self.points) == 1:
            return True

        return self.total_duration + order_duration + self.point_buffer <= self.max_capacity

    @property
    def point_buffer(self):
        return  10 * 60

    @property
    def latest_stop(self):
        return self.waypoints[-1]

    @property
    def start_point(self):
        return self.waypoints[0]

    def add_leg(self, leg):
        if self.latest_stop != leg.source:
            raise InvalidLeg

        self.points.append(leg.destination)
        leg.destination.assign_route(self)

        self.total_distance += leg.distance
        self.total_duration += leg.duration + self.point_buffer

# class PseudoRoute(AbstractRoute):
#     @property
#     def max_capacity(self):
#         return 180 * 60
#
#     def add_point(self, order, distance):
#         time = distance * 60
#         leg = Leg(self.latest_stop, order, distance, time)
#         super().add_leg(leg)
#
#
# class Route(AbstractRoute):
#     @classmethod
#     def from_psuedo_route(cls, psuedo_route, gapi):
# #         gapi = gmaps.GMaps()
#         legs = gapi.get_route(psuedo_route)
#         route = cls(legs[0].source)
#         for i, leg in enumerate(legs):
#             if route.can_add(leg):
#                 route.add_leg(leg)
#             else:
#                 break
#         # reset the assigned flag
#         if i != len(legs) - 1:
#             for leg in legs[i:]:
#                 leg.destination.unassign_route()
#
# #         Finally add the last leg from last order to distribution center
# #         final_leg = gapi.get_distance_between(route.latest_stop, route.start_point)
# #         route.add_leg(final_leg)
#
#         return route
#
#     @property
#     def max_capacity(self):
#         return 90 * 60
#
#     def can_add(self, leg):
#         return super().can_add(leg.duration)
#
#     def as_dict(self):
#         data = {'route_duration': self.total_duration,
#                 'route_distance': self.total_distance,
#                 'orders': []}
#
#
#         for order in self.points:
#             data['orders'].append({
#                     "order_id": order.id,
#                     "order_lat": order.lat,
#                     "order_long": order.long,
#                 })
#
#         return data
#
#


