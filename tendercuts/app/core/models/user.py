from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    flock_id = models.CharField(max_length=30, blank=True, null=True)
    store_id = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
