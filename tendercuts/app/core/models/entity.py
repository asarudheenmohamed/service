# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class EavAttribute(models.Model):
    attribute_id = models.SmallIntegerField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute_code = models.CharField(max_length=255, blank=True, null=True)
    attribute_model = models.CharField(max_length=255, blank=True, null=True)
    backend_model = models.CharField(max_length=255, blank=True, null=True)
    backend_type = models.CharField(max_length=8)
    backend_table = models.CharField(max_length=255, blank=True, null=True)
    frontend_model = models.CharField(max_length=255, blank=True, null=True)
    frontend_input = models.CharField(max_length=50, blank=True, null=True)
    frontend_label = models.CharField(max_length=255, blank=True, null=True)
    frontend_class = models.CharField(max_length=255, blank=True, null=True)
    source_model = models.CharField(max_length=255, blank=True, null=True)
    is_required = models.SmallIntegerField()
    is_user_defined = models.SmallIntegerField()
    default_value = models.TextField(blank=True, null=True)
    is_unique = models.SmallIntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eav_attribute'
        unique_together = (('entity_type', 'attribute_code'),)
        app_label = "magento"
