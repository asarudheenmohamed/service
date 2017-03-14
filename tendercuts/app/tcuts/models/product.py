# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from .entity import EavAttribute

import itertools
import collections
import sys

class CatalogProductEntity(models.Model):
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    # attribute_set = models.ForeignKey('EavAttributeSet', models.DO_NOTHING)
    entity_id = models.AutoField(primary_key=True)
    type_id = models.CharField(max_length=32)
    sku = models.CharField(max_length=64, blank=True, null=True)
    has_options = models.SmallIntegerField()
    required_options = models.SmallIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vtiger_id = models.IntegerField(blank=True, null=True)
    vtiger_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity'
        app_label = "magento"

class CatalogProductEntityDatetime(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.SmallIntegerField()
    attribute = models.ForeignKey(EavAttribute, models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    value = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_datetime'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = "magento"


class CatalogProductEntityDecimal(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.SmallIntegerField()
    attribute = models.ForeignKey(EavAttribute, models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING)
    value = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_decimal'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = "magento"


class CatalogProductEntityInt(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey(EavAttribute, models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING)
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_int'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = "magento"


class CatalogProductEntityText(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey(EavAttribute, models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_text'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = "magento"


class CatalogProductEntityVarchar(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey(EavAttribute, models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING, "varchars")
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_varchar'
        app_label = "magento"
        default_related_name = 'varchars'


class ProductStore():
    """
    Bloody!

    There is no straight forward way to create from the models, because the EAV model in magento
    is fucking stupid!

    So all this monkey patching to handle this!
    """

    _MAPPING = {
        "name": ("CatalogProductEntityVarchar", 71),
        "description": ("CatalogProductEntityText", 72),
        "short_description": ("CatalogProductEntityText", 73),
        "price": ("CatalogProductEntityDecimal", 75),
        "image": ("CatalogProductEntityVarchar", 85),
        "small_image": ("CatalogProductEntityVarchar", 86),
        "status": ("CatalogProductEntityInt", 96),
        "visibility": ("CatalogProductEntityInt", 102),
        "weight_description": ("CatalogProductEntityVarchar", 185),
        "gross_weight_description": ("CatalogProductEntityVarchar", 191),
        "uom": ("CatalogProductEntityInt", 193),
    }

    def get_store_product(self, store_id=0, attributes=None):
        if not attributes:
            attributes = list(self._MAPPING.keys())

        attributes = [self._MAPPING[attr] for attr in attributes]
        models_to_query = itertools.groupby(attributes, key=lambda x: x[0])

        products = CatalogProductEntity.objects.all()
        product_ids = [ pro.entity_id for pro in products]

        attributes_data = []
        for model_name, mappings in models_to_query:

            attribute_codes = [ mapping[1] for mapping in mappings ]
            model = getattr(sys.modules[__name__], model_name)

            attributes_data.extend(
                model.objects.filter(
                    store_id=store_id,
                    attribute_id__in=attribute_codes).
                    # entity_id__in=product_ids).
                select_related('attribute').
                order_by("entity_id"))

        data = collections.defaultdict(dict)
        for eav in attributes_data:
            data[eav.entity_id][eav.attribute.attribute_code] = eav.value

        return data.values()

