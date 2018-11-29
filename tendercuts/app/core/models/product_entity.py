# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CatalogProductEntityText(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey('CatalogProductEntity', models.DO_NOTHING)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_text'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = 'magento'


class CatalogProductEntityVarchar(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey('CatalogProductEntity', models.DO_NOTHING)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_varchar'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = 'magento'
