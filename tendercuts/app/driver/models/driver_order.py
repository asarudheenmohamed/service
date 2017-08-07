"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class DriverOrder(models.Model):
    """Order Assigment model."""

    driver_id = models.IntegerField(blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
