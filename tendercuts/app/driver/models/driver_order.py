"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class DriverOrder(models.Model):
    """Order Assigment model."""

    driver_id = models.IntegerField(blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


class DriverPosition(models.Model):
    """Driver Position model."""
    driver = models.ForeignKey(DriverOrder)
    latitude = models.FloatField(max_length=100)
    longitude = models.FloatField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class OrderEvents(models.Model):
    """Driver Events model."""
    driver_position = models.ForeignKey(DriverPosition)
    location = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=200)
