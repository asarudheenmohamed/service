"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

import datetime
import itertools

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from app.core.lib import cache
from django.contrib.auth.models import User


class DriverOrder(models.Model):
    """Order Assigment model."""

    def __unicode__(self):
        return '{}:{}'.format(self.increment_id, self.driver_id)

    driver_user = models.ForeignKey(User, blank=True, null=True)
    driver_id = models.IntegerField(blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)



class DriverTrip(models.Model):
    """Driver Trip Model."""
    driver_user = models.ForeignKey(User, blank=True, null=True)
    driver_order = models.ManyToManyField(DriverOrder)
    km_traveled = models.CharField(max_length=20, blank=True, null=True)
    km_travelled = models.FloatField(max_length=100, blank=True, null=True)
    trip_created_time = models.DateTimeField(default=timezone.now)
    trip_ending_time = models.DateTimeField(blank=True, null=True)
    trip_completed = models.BooleanField(default=False)

    @property
    def trip_starting_point(self):
        """Retrns the driver trip starting pints latitude and longitude."""

        key = 'starting_point:{}'.format(self.id)
        trip_starting_point = cache.get_key(key)

        if trip_starting_point:
            return trip_starting_point
        else:
            trip_starting_point = OrderEvents.objects.filter(
                driver_order__in=self.driver.all(),
                status='out_delivery').order_by('updated_time').prefetch_related('driver_position').first()

            return str(trip_starting_point.driver_position)

    @property
    def trip_ending_point(self):
        """Retrns the driver trip starting pints latitude and longitude."""
        key = 'ending_point:{}'.format(self.id)
        trip_ending_point = cache.get_key(key)

        if trip_ending_point:
            return trip_ending_point
        else:
            trip_ending_point = OrderEvents.objects.filter(
                driver_order__in=self.driver.all()).prefetch_related('driver_position').order_by('updated_time').last()

            return str(trip_ending_point.driver_position)


class DriverPosition(models.Model):
    """Driver Position model."""
    driver_user = models.ForeignKey(User, blank=True, null=True)
    driver_id = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(max_length=100)
    longitude = models.FloatField(max_length=100)
    recorded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{},{}".format(self.latitude, self.longitude)


class OrderEvents(models.Model):
    """Driver Events model."""
    driver = models.ForeignKey(DriverOrder)
    driver_position = models.ForeignKey(DriverPosition)
    updated_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)


class DriverStat(models.Model):
    """Driver Stat model."""
    driver_user = models.ForeignKey(User, blank=True, null=True)
    driver_id = models.IntegerField(blank=True, null=True)
    no_of_orders = models.IntegerField(default=0)
    km_travels = models.FloatField(blank=True, null=True)


class DriverLoginLogout(models.Model):
    """Driver Login Logout model."""
    driver = models.ForeignKey(User)
    date = models.DateField(default=datetime.date.today)
    check_in = models.TimeField(auto_now=True)
    check_out = models.TimeField(blank=True, null=True)
