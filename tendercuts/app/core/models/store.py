# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class GmapLangandlatisLongandlatis(models.Model):
    entity_id = models.AutoField(primary_key=True)
    storename = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    status = models.SmallIntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gmap_langandlatis_longandlatis'
        app_label = 'magento'


class GmapLangandlatisLongandlatisStore(models.Model):
    # Eventhough the field is different, it will hook correctly due to the
    # primary_key tag.
    longandlatis = models.ForeignKey(GmapLangandlatisLongandlatis, models.DO_NOTHING)

    # Break multiple foreign keys
    store_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'gmap_langandlatis_longandlatis_store'
        app_label = 'magento'
        # unique_together = (('longandlatis', 'store'),)


class CoreStore(models.Model):
    store_id = models.SmallIntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=32, blank=True, null=True)
    website_id = models.SmallIntegerField()
    # website = models.ForeignKey('CoreWebsite', models.DO_NOTHING)
    # group = models.ForeignKey('CoreStoreGroup', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    sort_order = models.SmallIntegerField()
    is_active = models.SmallIntegerField()

    # To_feild will be automatically picked up!
    location = models.ForeignKey(
            GmapLangandlatisLongandlatisStore,
            models.DO_NOTHING,
            db_column="store_id")

    class Meta:
        managed = False
        db_table = 'core_store'
        app_label = 'magento'
