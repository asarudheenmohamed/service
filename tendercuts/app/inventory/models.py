from __future__ import unicode_literals

import pytz

from django.contrib.auth.models import User

from app.core.models import CatalogProductFlat1
from app.core.models import AitocCataloginventoryStockItem

from django.db import models
from django.utils import timezone


class NotifyCustomer(models.Model):
    """Order Assigment model."""

    customer = models.ForeignKey(User)
    product_id = models.IntegerField(blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField(default=timezone.now().replace(
                    hour=20, minute=0, second=0, microsecond=0, tzinfo=pytz.utc))