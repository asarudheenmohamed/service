"""Model that contains Customers Notification."""
from __future__ import unicode_literals

import pytz
from django.contrib.auth.models import User
from enum import Enum
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

    class Status(Enum):
        CREATED = 0
        APPROVED = 1
        REJECTED = 2

    class INV_TYPE(Enum):
        TODAY = 0
        TOMO  = 1

    """Model for inventory request"""
    created_time = models.DateTimeField(default=timezone.now)

    product_id = models.IntegerField(blank=False)
    product_name = models.CharField(max_length=300, blank=False)
    sku = models.CharField(max_length=300, blank=False)

    store_id = models.IntegerField(blank=False)
    store_name = models.CharField(max_length=300, blank=False)

    type = models.SmallIntegerField(blank=False)
    qty = models.IntegerField(blank=False)
    triggered_by = models.ForeignKey(User, related_name='triggered_by')
    approved_by = models.ForeignKey(User, blank=True, null=True, related_name='approved_by')
    # 0 -> Pending, 1 -> Approved, 2 - Rejected
    status = models.SmallIntegerField(default=0)


class Inventorylog(models.Model):
    inventorylogid = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    relatedto = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    adminuser = models.CharField(max_length=255, blank=True, null=True)
    revert = models.CharField(max_length=255, blank=True, null=True)
    stockupdatedfrom = models.CharField(max_length=255, blank=True, null=True)
    stockupdatedto = models.CharField(max_length=255, blank=True, null=True)
    store_id = models.CharField(max_length=255, blank=True, null=True)
    type_of_qty = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        app_label = "magento"
        db_table = 'inventorylog'
