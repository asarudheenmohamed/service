"""Automatically controls the trip of the driver"""
import logging
import sys
import traceback
from datetime import date, datetime, timedelta

from django.conf import settings
from django.utils import timezone

import googlemaps
from app.core.lib import cache
from app.core.lib.communication import Mail
from app.core.models import SalesFlatOrder
from app.driver.models.driver_order import (DriverPosition, DriverTrip,
                                            OrderEvents)


class TripController:
    PREFIX = "trip"
    TRIP_STARTING_POINT_PREFIX = 'starting_point'
    TRIP_ENDING_POINT_PREFIX = 'ending_point'

    def __init__(self, log=None, driver=None):
        self.log = log or logging.getLogger()
        self._api = googlemaps.Client(
            key=settings.GOOGLE_MAP_DISTANCE_API['KEY'])
        self.driver = driver

    def _get_key(self):
        """Set driver trip cache key.

        Params:
         order: driver order object

        """
        return "{}:{}".format(self.PREFIX, self.driver.username)

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
        trip_orders = trip.driver_order.all()
        if trip_orders:

            self.log.info("Completing the trip for driver {}".format(trip.id))
            trip.trip_completed = True
            trip.trip_ending_time = timezone.now()
            trip.status = 2
            trip.save()
            self.compute_driver_trip_distance(trip)
        else:
            trip.delete()

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
            if (status == 'canceled' or status == 'closed'):
                driver_order = trip.driver_order.filter(
                    increment_id=order_id).first()
                trip.driver_order.remove(driver_order)
                continue

            if status == 'out_delivery':
                return False

        return True

    def check_and_create_trip(self, order, driver_position, trip_id):
        """Check if a trip is available or generates a TRIP.
        param :
            order:(DriverObject): Driver object
            trip_id(int):auto generated trip id

        :return: DriverTrip
        """
        key = self._get_key()
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
                # re-run the logic
                return self.check_and_create_trip(order, driver_position,trip_id)

        elif trip_id is None:
            self.log.debug("Creating a new trip for the driver {}".format(
                order.driver_id))
            trip = DriverTrip.objects.create(driver_user=self.driver)
            cache.set_key(key, trip.id, 60 * 60 * 24)  # 1 day
            trip_starting_point = self.generate_trip_starting_point_key(
                trip.id)

            cache.set_key(
                trip_starting_point,
                str(driver_position),
                60 * 60 * 24)  # expired at 1 day
        else:
            # Get the driver current auto generated trip object
            trip = DriverTrip.objects.get(pk=trip_id)

        # add driver trip assign orders
        trip.driver_order.add(order)
        trip_driver_orders = trip.driver_order.all()

        # update order sequence number
        SalesFlatOrder.objects.filter(
            increment_id=order.increment_id).update(
            sequence_number=len(trip_driver_orders))

        return trip

    def update_sequence_number(self, order_id, sequence_number):
        """Update order sequence number for the given order id.

        Params:
            order_id(str): order increment_id
            sequence_number(str): order sequence number

        """
        trip_obj = DriverTrip.objects.get(
            driver_order__increment_id=order_id)
        order_ids = list(
            trip_obj.driver_order.all().values_list(
                'increment_id', flat=True))

        order_objects = SalesFlatOrder.objects.filter(
            increment_id__in=order_ids,
            sequence_number__gte=sequence_number)
        order_ids = list(order_objects.values_list(
            'increment_id', flat=True).order_by('sequence_number'))

        # for the given order id moves to last index
        order_ids.append(order_ids.pop(order_ids.index(order_id)))
        for index, value in enumerate(order_ids, start=sequence_number):
            order = order_objects.get(increment_id=value)
            order.sequence_number = index
            order.save()

    def fetch_driver_trip(self, driver):
        """Return a last 10 days driver trip."""
        start_date = timezone.now() - timezone.timedelta(days=10)
        driver_trip = DriverTrip.objects.filter(driver_user=driver, trip_created_time__range=(
            start_date, datetime.now()))

        return driver_trip

    def check_and_complete_trip(self, order, driver_position, trip_id=None):
        """Check if a trip is available and completes a TRIP.
        :param
            order:(DriverObject): Driver object
            trip_id(int): Auto generated trip_id

        :return: trip object
        """

        key = self._get_key()
        if trip_id:
            trip = trip_id
        else:
            # get current trip
            trip = cache.get_key(key)

        # fail if a trip is not found.
        if not trip:
            raise ValueError("Trip error not found for order id {}".format(
                order.increment_id))

        trip = DriverTrip.objects.get(pk=trip)

        if self._can_complete_trip(trip):
            self._complete_trip(trip)
            if trip_id:
                return trip
            # delete the key
            cache.delete_key(key)

            trip_ending_point = self.generate_trip_ending_point_key(
                trip.id)

            cache.set_key(
                trip_ending_point,
                str(driver_position),
                60 * 60 * 24)  # expired at 1 day

        return trip

    def fetch_order_events(self, trip):
        """Fetch order events objects.

        Args:
           trip (obj): driver trip object

        """
        order_events = OrderEvents.objects.filter(driver__in=trip.driver_order.all(
        )).prefetch_related('driver_position').order_by('updated_time')

        return order_events

    def _get_way_points(self, trip_starting_time,
                        order_event_complete_objects, driver_user):
        """"""
        way_points = []

        for event_complete_object in order_event_complete_objects:

            # fetch driver position
            position_objects = DriverPosition.objects.filter(
                driver_user=driver_user, recorded_time__range=(
                    trip_starting_time, event_complete_object.updated_time))
            # mid index of driver position
            mid_index = len(position_objects) / 2
            # mid position
            try:
                mid_position = position_objects[mid_index]
                way_points.append(str(mid_position))
                way_points.append(str(event_complete_object.driver_position))
            except:
                pass

            trip_starting_time = event_complete_object.updated_time

        return way_points

    def get_directions_km(self, starting_points,
                          destination_point,
                          way_points, trip_id):
        """Compute the km based on particular directions latitude and longitude.

        Args:
            starting_points(str): trip starting point
            destination_point(str): trip destination_point
            way_points(str): trip way_points

        returns:
            direction distance(meter)

          """
        km_travelled = 0

        try:

            compute_km = scompute_km = self._api.directions(starting_points, destination_point,
                                                            waypoints=way_points)

            self.log.info(
                'Measured the km taken for the trip by the driver using google api with way points travlled from starting point :{} to ending point :{} for a trip '.format(
                    starting_points, destination_point))

            km_travelled = 0

            for leg in compute_km[0]['legs']:
                km_travelled += int(leg['distance']['value'])

        except Exception as msg:
            message = 'Error:{}, trip_id:{},waypoints:{},starting points:{},destination point:{}'.format(
                repr(msg), trip_id, way_points, starting_points, destination_point)
            self.log.error('{}, trip_id:{}'.format(repr(msg), trip_id))

            # send error message in tech support mail
            Mail().send(
                "reports@tendercuts.in",
                ["tech@tendercuts.in"],
                "[CRITICAL] Error in Driver Trip distance computaion",
                message)

        return km_travelled

    def _split(self, waypoints, index):
        """Split the waypoints based on index."""
        ways = []
        while len(waypoints) > index:
            pice = waypoints[:index]

            ways.append(pice)
            waypoints = waypoints[index:]
        ways.append(waypoints)

        return ways

    def compute_driver_trip_distance(self, trip):
        """Update the km taken by the driver for each trip.

        Params:
           trip(obj): completed driver trip object

        """
        # based on lat long distance has been measured for each trip taken by
        # the driver

        # driver trip starting point

        order_events = self.fetch_order_events(trip)

        # starting and ending destination point
        starting_points = str(order_events.first().driver_position)
        destination_point = str(order_events.last().driver_position)

        # trip starting point
        trip_starting_time = order_events.first().updated_time

        # sort completed order only because we get a order completed
        # location and completed time
        order_event_complete_objects = order_events.filter(
            status='completed').order_by('updated_time')

        way_points = self._get_way_points(
            trip_starting_time, order_event_complete_objects, trip.driver_user)

        split_way = self._split(way_points, 22)

        km_travelled = 0

        for waypoints in split_way:
            try:
                destination = waypoints[-1]
            except IndexError:
                destination = destination_point

            distance = self.get_directions_km(
                starting_points, destination_point, waypoints, trip.id)

            starting_point = destination

            km_travelled += distance

        trip.km_travelled = km_travelled

        trip.save()
