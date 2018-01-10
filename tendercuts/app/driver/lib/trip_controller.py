"""Automatically controls the trip of the driver"""
import logging

import googlemaps
from django.conf import settings
from django.utils import timezone

from app.core.lib import cache
from app.core.models import SalesFlatOrder
from app.driver.models.driver_order import DriverTrip
import sys
import traceback


class TripController:
    PREFIX = "trip"
    TRIP_STARTING_POINT_PREFIX = 'starting_point'
    TRIP_ENDING_POINT_PREFIX = 'ending_point'

    def __init__(self, log=None):
        self.log = log or logging.getLogger()
        self._api = googlemaps.Client(
            key=settings.GOOGLE_MAP_DISTANCE_API['KEY'])

    def _get_key(self, order):
        """Set driver trip cache key.

        Params:
         order: driver order object

        """

        return "{}:{}".format(self.PREFIX, order.driver_id)

    def generate_trip_starting_point_key(self, trip_id):
        """Set driver trip starting point cache key.

        Params:
         order: driver trip id

        """

        return "{}:{}".format(self.TRIP_STARTING_POINT_PREFIX, trip_id)

    def generate_trip_ending_point_key(self, trip_id):
        """Set driver trip ending point cache key.

        Params:
         order: driver trip id

        """

        return "{}:{}".format(self.TRIP_ENDING_POINT_PREFIX, trip_id)

    def _complete_trip(self, trip):
        """Complete driver trip.

        Params:
          trip(obj): driver trip object

        """
        self.log.info("Completing the trip for driver {}".format(trip.id))
        trip.trip_completed = True
        trip.trip_ending_time = timezone.now()
        trip.save()
        self.compute_driver_trip_distance(trip)

    def _can_complete_trip(self, trip):
        """Check if the trip can be completed.

        :param trip: DriverTrip
        :return: DriverTrip or None if completed

        """
        # check if all orders are complete.
        order_ids = trip.driver_order.values_list('increment_id', flat=True)
        orders = SalesFlatOrder.objects.filter(increment_id__in=list(order_ids)) \
            .values_list('increment_id', 'status')

        if not orders:
            return False

        for order_id, status in orders:
            # if the status is complete, continue
            if status == 'complete':
                continue

            # remove and continue.
            if status == 'canceled':
                driver_order = trip.driver_order.filter(
                    increment_id=order_id).first()
                trip.driver_order.remove(driver_order)
                continue

            if status == 'out_delivery':
                return False

        return True

    def check_and_create_trip(self, order, driver_position):
        """Check if a trip is available or generates a TRIP.
        :param order:(DriverObject): Driver object

        :return: DriverTrip
        """
        key = self._get_key(order)
        self.log.debug(
            "Creating/updating a trip for {}".format(order.increment_id))

        if cache.get_key(key):
            self.log.debug("Found an exiting trip for the driver {}".format(
                order.driver_id))
            trip = DriverTrip.objects.get(pk=cache.get_key(key))
            # Completing the old trip here, since the is a chance that it might
            # be stale, edge case where the driver trip's last order gets cancelled
            # and the trip might remain stale.
            if self._can_complete_trip(trip):
                self._complete_trip(trip)
                # delete the key
                cache.delete_key(key)
                trip_ending_point = self.generate_trip_ending_point_key(
                    trip.id)
                # re-run the logic
                return self.check_and_create_trip(order, driver_position)

        self.log.debug("Creating a new trip for the driver {}".format(
            order.driver_id))
        trip = DriverTrip.objects.create()
        cache.set_key(key, trip.id, 60 * 60 * 24)  # 1 day
        trip_starting_point = self.generate_trip_starting_point_key(
            trip.id)

        cache.set_key(
            trip_starting_point,
            str(driver_position),
            60 * 60 * 24)  # expired at 1 day
        # create driver trip
        trip.driver_order.add(order)

        return trip

    def check_and_complete_trip(self, order, driver_position):
        """Check if a trip is available and completes a TRIP.
        :param order:(DriverObject): Driver object

        :return: none
        """

        key = self._get_key(order)

        # get current trip
        trip = cache.get_key(key)
        # fail if a trip is not found.
        if not trip:
            raise ValueError("Trip error not found for order id {}".format(
                order.increment_id))

        trip = DriverTrip.objects.get(pk=cache.get_key(key))

        if self._can_complete_trip(trip):
            self._complete_trip(trip)
            # delete the key
            cache.delete_key(key)

            trip_ending_point = self.generate_trip_ending_point_key(
                trip.id)

            cache.set_key(
                trip_ending_point,
                str(driver_position),
                60 * 60 * 24)  # expired at 1 day
        return trip

    def compute_driver_trip_distance(self, trip):
        """Update the km taken by the driver for each trip.

        Params:
           trip(obj): completed driver trip object

        """
        # based on lat long distance has been measured for each trip taken by
        # the driver

        # driver trip starting point
        starting_points = trip.trip_starting_point
        ending_points = trip.trip_ending_point
        # way point holds atleast one points for the each order
        way_points = []
        for order in trip.driver_order.all():
            order_way_points = order.way_points
            mid_point = len(order_way_points) / 2
            way_points.append(str(order_way_points[mid_point]))
            way_points.append(str(order_way_points.last()))

        try:
            compute_km = self._api.directions(starting_points, ending_points,
                                              waypoints=way_points)

            self.log.info(
                'Measured the km taken for the trip by the driver using google api with way points travlled from starting point :{} to ending point :{} for a trip '.format(
                    starting_points, ending_points))

            # update trip km
            trip.km_traveled = compute_km[0]['legs'][0]['distance']['text']

            trip.save()

        except Exception as msg:
            self.log.error(
                '{}, trip_id:{}'.format(
                    repr(
                        msg),
                    trip.id))
            pass
