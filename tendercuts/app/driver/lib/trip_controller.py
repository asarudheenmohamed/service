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
from app.driver.lib import DriverTripController


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
            DriverTripController(trip).compute_driver_trip_distance()
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

    def check_and_create_trip(self, order, driver_position):
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
                return self.check_and_create_trip(
                    order, driver_position)

        else:
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
        # add driver trip assign orders
        trip.driver_order.add(order)
        trip_driver_orders = trip.driver_order.all()

        # update order sequence number
        SalesFlatOrder.objects.filter(
            increment_id=order.increment_id).update(
            sequence_number=len(trip_driver_orders))

        return trip

    def fetch_driver_trip(self, driver):
        """Return a last 10 days driver trip."""
        start_date = timezone.now() - timezone.timedelta(days=10)
        driver_trip = DriverTrip.objects.filter(driver_user=driver, trip_created_time__range=(
            start_date, datetime.now()))

        return driver_trip

    def check_and_complete_trip(self, order, driver_position):
        """Check if a trip is available and completes a TRIP.
        :param
            order:(DriverObject): Driver object
            trip_id(int): Auto generated trip_id

        :return: trip object
        """

        key = self._get_key()
        # get current trip
        trip = cache.get_key(key)

        # fail if a trip is not found.
        if not trip:
            raise ValueError("Trip error not found for order id {}".format(
                order.increment_id))

        trip = DriverTrip.objects.get(pk=trip)

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
