"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

from django.db import models


class GoogleGeocode(models.Model):
    """Order Assigment model."""

    query = models.TextField(db_index=True, max_length=500)
    latitude = models.CharField(max_length=25)
    longitude = models.CharField(max_length=25)
    location_type = models.CharField(max_length=25)
    area = models.FloatField()
