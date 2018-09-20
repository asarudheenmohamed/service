from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    flock_id = models.CharField(max_length=30)
    store_id = models.IntegerField()
    phone = models.CharField(max_length=12)
