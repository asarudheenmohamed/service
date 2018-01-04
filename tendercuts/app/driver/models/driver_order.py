"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class DriverOrder(models.Model):
    """Order Assigment model."""

    def __unicode__(self):
        return '{}:{}'.format(self.increment_id, self.driver_id)

    driver_id = models.IntegerField(blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class DriverTrip(models.Model):
    """Driver Trip Model."""
    driver_order = models.ManyToManyField(DriverOrder)
    km_traveled = models.CharField(max_length=20, blank=True, null=True)
    trip_created_time = models.DateTimeField(default=timezone.now)
    trip_ending_time = models.DateTimeField(blank=True, null=True)
    trip_completed = models.BooleanField(default=False)

    @property
    def trip_starting_point(self):
        """Retrns the driver trip starting pints latitude and longitude."""

        trip_starting_point = OrderEvents.objects.filter(
            driver=self.driver_order.all().first(),
            status='out_delivery').prefetch_related('driver_position')[0]

        return '{},{}'.format(trip_starting_point.driver_position.latitude,
                              trip_starting_point.driver_position.longitude)

    @property
    def way_and_destination_points(self):
        """Returns the driver destination points and way points."""

        trip_way_point_obj = OrderEvents.objects.filter(
            driver__in=self.driver_order.all(),
            status='completed').order_by('updated_time')

        # get trip last point
        dest_point_obj = trip_way_point_obj.last()

        destination_point = '{},{}'.format(
            dest_point_obj.driver_position.latitude, dest_point_obj.driver_position.longitude)

        way_points = ['{},{}'.format(
            trip_way_point.driver_position.latitude,
            trip_way_point.driver_position.longitude)
            for trip_way_point in trip_way_point_obj]

        return {"destination_point": destination_point,
                "way_points": way_points}


class DriverPosition(models.Model):
    """Driver Position model."""
    driver_id = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(max_length=100)
    longitude = models.FloatField(max_length=100)
    recorded_time = models.DateTimeField(auto_now_add=True)


class OrderEvents(models.Model):
    """Driver Events model."""
    driver = models.ForeignKey(DriverOrder)
    driver_position = models.ForeignKey(DriverPosition)
    updated_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)


class DriverStat(models.Model):
    """Driver Stat model."""
    driver_id = models.IntegerField(blank=True, null=True)
    no_of_orders = models.IntegerField(default=0)
    km_travels = models.FloatField(blank=True, null=True)
