# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CustomerAddressEntity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_type_id = models.SmallIntegerField()
    attribute_set_id = models.SmallIntegerField()
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey("CustomerEntity", models.DO_NOTHING, blank=True, null=True, related_name="addresses")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_active = models.SmallIntegerField()
    vtiger_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_address_entity'
        app_label = "magento"


class CustomerAddressEntityDatetime(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerAddressEntity, models.DO_NOTHING, related_name="dates")
    value = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_address_entity_datetime'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerAddressEntityDecimal(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerAddressEntity, models.DO_NOTHING, related_name="decimal")
    value = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'customer_address_entity_decimal'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerAddressEntityInt(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerAddressEntity, models.DO_NOTHING, related_name="ints")
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customer_address_entity_int'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerAddressEntityText(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerAddressEntity, models.DO_NOTHING, related_name="texts")
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'customer_address_entity_text'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerAddressEntityVarchar(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerAddressEntity, models.DO_NOTHING, related_name="varchars")
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_address_entity_varchar'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"
