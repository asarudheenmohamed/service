

from django.db import models

from django.contrib.auth.models import User


class OrderTimelapse(models.Model):
    """Order  lapse model."""

    driver_user = models.ForeignKey(User, blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    processing_time = models.DateTimeField(blank=True, null=True)
    out_delivery_time = models.DateTimeField(blank=True, null=True)
    completed_time = models.DateTimeField(blank=True, null=True)
    pending_lapse = models.IntegerField(blank=True, null=True)
    processing_lapse = models.IntegerField(blank=True, null=True)
    out_delivery_lapse = models.IntegerField(blank=True, null=True)
    deliverytype = models.IntegerField(blank=True, null=True)
