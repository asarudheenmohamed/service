# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DriverManagement(models.Model):
    entity_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    store = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    address = models.TextField()
    photo = models.CharField(max_length=222)
    id_proof = models.TextField()
    ref1_name = models.CharField(max_length=100)
    ref1_phone = models.CharField(max_length=15)
    ref1_address = models.TextField()
    ref2_name = models.CharField(max_length=100)
    ref2_phone = models.CharField(max_length=15)
    ref2_address = models.TextField()
    created_date = models.DateField()
    status = models.IntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'driver_management'
        app_label = "magento"

    def make_inactive(self):
        self.status = 0

    def make_active(self):
        self.status = 1

    def make_available(self):
        self.status = 2

    def make_busy(self):
        self.status = 3

    def make_returning_back(self):
        self.status = 4


# class Driver(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     driver_id = models.IntegerField(null=True)

#     # @property
#     # def data(self):
#     #     return DriverManagement.objects.get(entity_id=driver_id)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Driver.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

