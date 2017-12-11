"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class DriverOrder(models.Model):
    """Order Assigment model."""

    driver_id = models.IntegerField(blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class DriverTrip(models.Model):
    """Driver Trip Model."""
    driver_order = models.ManyToManyField(DriverOrder)
    km_traveled = models.FloatField(blank=True, null=True)
    trip_created_time = models.DateTimeField(default=timezone.now)
    trip_ending_time = models.DateTimeField(blank=True, null=True)


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
