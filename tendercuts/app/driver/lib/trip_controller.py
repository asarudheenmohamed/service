"""Automatically controls the trip of the driver"""
import logging

from app.core.lib import cache
from app.driver.models import DriverTrip, OrderEvents
from app.core.models import SalesFlatOrder
from django.utils import timezone
import googlemaps


class TripController:
    PREFIX = "trip"

    def __init__(self, log=None):
        self.log = log or logging.getLogger()
        self._api = googlemaps.Client(
            key='AIzaSyCQK2O4AMogjO323B-6btf9f2krVWST3bU')

    def _get_key(self, order):
        """Set driver trip cache key.

        Params:
         order: driver order object

        """

        return "{}:{}".format(self.PREFIX, order.driver_id)

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

    def check_and_create_trip(self, order):
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
                # re-run the logic
                self.check_and_create_trip(order)
        else:
            self.log.debug("Creating a new trip for the driver {}".format(
                order.driver_id))
            trip = DriverTrip.objects.create()
            cache.set_key(key, trip.id, 60 * 60 * 24)  # 1 day

        # create driver trip
        trip.driver_order.add(order)

        return trip

    def check_and_complete_trip(self, order):
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

        return trip

    def compute_driver_trip_distance(self, trip):
        """Update the km taken by the driver for each trip.

        Params:
           trip(obj): completed driver trip object

        """

        order_event_objects = OrderEvents.objects.filter(driver__in=trip.driver_order.all(
        )).order_by('updated_time').prefetch_related('driver_position')

        self.log.info(
            'Fetched the trip:{} events lat and longs'.format(
                trip.id))

        # get the driver starting location
        driver_strting_position = order_event_objects.filter(
            status='out_delivery').last()

        driver_position_objs = [
            order_event.driver_position for order_event in order_event_objects]

        # based on lat long distance has been measured for each trip taken by
        # the driver
        compute_km = self._api.directions("{},{}".format(driver_strting_position.driver_position.latitude, driver_strting_position.driver_position.longitude), "{},{}".format(driver_position_objs[
            -1].latitude, driver_position_objs[-1].longitude),
            waypoints=["{},{}|".format(i.latitude, i.longitude)
                       for i in driver_position_objs[1:-1]])

        self.log.info(
            'Measured the km taken for the trip by the driver using google api with way points travlled from starting point :lat:{},long:{} to ending point :lat:{},long:{} for a trip '.format(
                driver_strting_position.driver_position.latitude, driver_strting_position.driver_position.longitude, driver_position_objs[
                    0].latitude, driver_position_objs[0].longitude))

        # update trip km
        trip.km_traveled = compute_km[0]['legs'][0]['distance']['text']

        trip.save()
