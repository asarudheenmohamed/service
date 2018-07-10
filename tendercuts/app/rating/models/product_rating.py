"""Model that contains the assignment of driver to order."""

from __future__ import unicode_literals

import datetime
import itertools

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from app.core.lib import cache
from django.contrib.auth.models import User


class RatingTag(models.Model):
    """Rating Tags for product."""

    tag_name = models.CharField(max_length=50, blank=True, null=True)
    threshold = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        """Returns to tag name"""
        return self.tag_name


class Rating(models.Model):
    """Order Rating model."""

    customer = models.ForeignKey(User, blank=True, null=True)
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=250, blank=True, null=True)
    rating_tag = models.ManyToManyField(RatingTag, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
