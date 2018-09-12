"""Model that contains Customers Notification."""
from __future__ import unicode_literals

import pytz
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from app.core.models import AitocCataloginventoryStockItem, CatalogProductFlat1


class NotifyCustomer(models.Model):
    """Order Assigment model."""

    customer = models.ForeignKey(User)
    product_id = models.IntegerField(blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField(
        default=timezone.now().replace(
            hour=20, minute=0, second=0, microsecond=0, tzinfo=pytz.utc))
    is_notified = models.BooleanField(default=False)


class InventoryRequest(models.Model):
    """Model for inventory request"""
    created_time = models.DateTimeField(default=timezone.now)
    product_id = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    triggered_by = models.ForeignKey(User)
    approved_by = models.ForeignKey(User)
    is_done = models.BooleanField(default=False)
