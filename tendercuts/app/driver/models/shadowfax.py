from __future__ import unicode_literals

from django.db import models
import math

class ShadowFaxUpdates(models.Model):
    rider_name = models.CharField(max_length=200, blank=True, null=True)
    rider_contact = models.CharField(max_length=200, blank=True, null=True)
    sfx_order_id = models.CharField(max_length=32)
    client_order_id = models.CharField(max_length=32)
    order_status = models.CharField(max_length=32)
    updated = models.DateTimeField(auto_now=True)

