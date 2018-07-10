# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class StockWarehouse(models.Model):
    name = models.CharField(max_length=-1)
    active = models.NullBooleanField()
    code = models.CharField(max_length=5)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    mage_code = models.CharField(max_length=-1, blank=True, null=True)
    mage_pos_code = models.CharField(max_length=-1, blank=True, null=True)
    flock_group_id = models.CharField(max_length=-1, blank=True, null=True)
    latitude = models.CharField(max_length=-1, blank=True, null=True)
    longitude = models.CharField(max_length=-1, blank=True, null=True)
    bigbasket_id = models.CharField(max_length=-1, blank=True, null=True)
    swipemachine_id = models.CharField(max_length=-1, blank=True, null=True)
    path_string = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_warehouse'
        unique_together = (('code', 'company'), ('name', 'company'),)
        app_label = "erp"


class StockWarehouseTcMapViewGeohashRel(models.Model):
    stock_warehouse = models.ForeignKey(StockWarehouse, models.DO_NOTHING, primary_key=True)
    tc_map_view_geohash = models.ForeignKey('TcMapViewGeohash', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'stock_warehouse_tc_map_view_geohash_rel'
        unique_together = (('stock_warehouse', 'tc_map_view_geohash'),)
        app_label = "erp"


class TcMapViewGeohash(models.Model):
    hash_id = models.CharField(unique=True, max_length=-1, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tc_map_view_geohash'
        app_label = "erp"
