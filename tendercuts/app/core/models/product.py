# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


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

    def __str__(self):              # __unicode__ on Python 2
        return str(self.entity_id)


class CatalogProductFlat(models.Model):
    entity = models.ForeignKey(
        CatalogProductEntity, models.DO_NOTHING, primary_key=True)
    attribute_set_id = models.SmallIntegerField()
    type_id = models.CharField(max_length=32)
    cost = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    gift_message_available = models.SmallIntegerField(blank=True, null=True)
    has_options = models.SmallIntegerField()
    image_label = models.CharField(max_length=255, blank=True, null=True)
    is_recurring = models.SmallIntegerField(blank=True, null=True)
    links_purchased_separately = models.IntegerField(blank=True, null=True)
    links_title = models.CharField(max_length=255, blank=True, null=True)
    msrp = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    msrp_display_actual_price_type = models.CharField(
        max_length=255, blank=True, null=True)
    msrp_enabled = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    news_from_date = models.DateTimeField(blank=True, null=True)
    news_to_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    price_type = models.IntegerField(blank=True, null=True)
    price_view = models.IntegerField(blank=True, null=True)
    recurring_profile = models.TextField(blank=True, null=True)
    required_options = models.SmallIntegerField()
    shipment_type = models.IntegerField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=64, blank=True, null=True)
    sku_type = models.IntegerField(blank=True, null=True)
    small_image = models.CharField(max_length=255, blank=True, null=True)
    small_image_label = models.CharField(max_length=255, blank=True, null=True)
    special_from_date = models.DateTimeField(blank=True, null=True)
    special_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    special_to_date = models.DateTimeField(blank=True, null=True)
    tax_class_id = models.IntegerField(blank=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_label = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    url_key = models.CharField(max_length=255, blank=True, null=True)
    url_path = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.SmallIntegerField(blank=True, null=True)
    weight = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weight_type = models.IntegerField(blank=True, null=True)
    credit_amount = models.TextField(blank=True, null=True)
    credit_rate = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gross_weight_description = models.CharField(
        max_length=255, blank=True, null=True)
    product_sold = models.IntegerField(blank=True, null=True)
    product_sold_value = models.CharField(
        max_length=255, blank=True, null=True)
    product_spec = models.CharField(max_length=255, blank=True, null=True)
    qty_inc = models.CharField(max_length=255, blank=True, null=True)
    rewardpoints_spend = models.IntegerField(blank=True, null=True)
    samples_title = models.CharField(max_length=255, blank=True, null=True)
    scheduledqty = models.IntegerField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    uom = models.IntegerField(blank=True, null=True)
    uom_value = models.CharField(max_length=255, blank=True, null=True)
    weight_description = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        app_label = "magento"
        abstract = True

    @property
    def thumb(self):
        """
        Append URL
        """
        return "{}/media/catalog/product/{}".format(settings.CDN, self.small_image)


class CatalogProductFlat1(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_1'
        app_label = "magento"


class CatalogProductFlat4(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_4'
        app_label = "magento"


class CatalogProductFlat5(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_5'
        app_label = "magento"


class CatalogProductFlat7(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_7'
        app_label = "magento"


class CatalogProductFlat8(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_8'
        app_label = "magento"


class CatalogProductFlat9(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_9'
        app_label = "magento"


class CatalogProductFlat10(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_10'
        app_label = "magento"


class CatalogProductFlat11(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_11'
        app_label = "magento"


class CatalogProductFlat12(CatalogProductFlat):
    class Meta:
        managed = False
        db_table = 'catalog_product_flat_12'
        app_label = "magento"