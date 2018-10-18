# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from __future__ import unicode_literals

from .product import CatalogProductEntity
from django.conf import settings
from django.db import models


class CatalogCategoryEntity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_type_id = models.SmallIntegerField()
    attribute_set_id = models.SmallIntegerField()
    parent_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    path = models.CharField(max_length=255)
    position = models.IntegerField()
    level = models.IntegerField()
    children_count = models.IntegerField()

    # TODO
    products = models.ManyToManyField(CatalogProductEntity,
                                      through="CatalogCategoryProduct",
                                      # db_table="catalog_category_product",
                                      through_fields=("category", "product"))
    # through_fields=("category", "product"))
    # related_name='categories',)
    # related_query_name='entity_id')

    def __str__(self):              # __unicode__ on Python 2
        return str(self.entity_id)

    class Meta:
        managed = False
        db_table = 'catalog_category_entity'
        app_label = "magento"


class CatalogCategoryProduct(models.Model):
    category = models.ForeignKey(
        CatalogCategoryEntity, models.DO_NOTHING,
        db_column="category_id", primary_key=True,
        to_field="entity_id")
    product = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING,
                                db_column="product_id", primary_key=True, to_field="entity_id")
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'catalog_category_product'
        unique_together = (('category', 'product'),)
        app_label = "magento"


class CatalogCategoryFlatStore(models.Model):
    entity = models.ForeignKey(
        CatalogCategoryEntity, models.DO_NOTHING, primary_key=True)
    parent_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    path = models.CharField(max_length=255)
    position = models.IntegerField()
    level = models.IntegerField()
    children_count = models.IntegerField()
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    all_children = models.TextField(blank=True, null=True)
    available_sort_by = models.TextField(blank=True, null=True)
    children = models.TextField(blank=True, null=True)
    creareseo_heading = models.CharField(max_length=255, blank=True, null=True)
    custom_apply_to_products = models.IntegerField(blank=True, null=True)
    custom_design = models.CharField(max_length=255, blank=True, null=True)
    custom_design_from = models.DateTimeField(blank=True, null=True)
    custom_design_to = models.DateTimeField(blank=True, null=True)
    custom_layout_update = models.TextField(blank=True, null=True)
    custom_use_parent_settings = models.IntegerField(blank=True, null=True)
    default_sort_by = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    display_mode = models.CharField(max_length=255, blank=True, null=True)
    filter_price_range = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    # overriding the magneto image!!
    # image = models.CharField(max_length=255, blank=True, null=True)
    include_in_menu = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    is_anchor = models.IntegerField(blank=True, null=True)
    landing_page = models.IntegerField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    page_layout = models.CharField(max_length=255, blank=True, null=True)
    path_in_store = models.TextField(blank=True, null=True)
    url_key = models.CharField(max_length=255, blank=True, null=True)
    url_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "magento"
        abstract = True

    @property
    def thumb(self):
        """
        Append URL: png image for the samll icons
        """
        return "{}/media/catalog/category/{}.png".format(settings.CDN, self.entity_id)

    @property
    def image(self):
        """
        Append URL: jpg image for the actual image
        """
        return "{}/media/catalog/category/{}.jpg".format(settings.CDN, self.entity_id)


class CatalogCategoryFlatStore1(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_1'
        app_label = "magento"


class CatalogCategoryFlatStore4(CatalogCategoryFlatStore):

    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_4'
        app_label = "magento"


class CatalogCategoryFlatStore5(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_5'
        app_label = "magento"


class CatalogCategoryFlatStore7(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_7'
        app_label = "magento"


class CatalogCategoryFlatStore8(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_8'
        app_label = "magento"


class CatalogCategoryFlatStore9(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_9'
        app_label = "magento"


class CatalogCategoryFlatStore10(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_10'
        app_label = "magento"


class CatalogCategoryFlatStore11(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_11'
        app_label = "magento"


class CatalogCategoryFlatStore12(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_12'
        app_label = "magento"

class CatalogCategoryFlatStore14(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_14'
        app_label = "magento"

class CatalogCategoryFlatStore15(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_15'
        app_label = "magento"

class CatalogCategoryFlatStore16(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_16'
        app_label = "magento"

class CatalogCategoryFlatStore18(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_18'
        app_label = "magento"

class CatalogCategoryFlatStore21(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_21'
        app_label = "magento"

class CatalogCategoryFlatStore24(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_24'
        app_label = "magento"

class CatalogCategoryFlatStore26(CatalogCategoryFlatStore):
    class Meta:
        managed = False
        db_table = 'catalog_category_flat_store_26'
        app_label = "magento"
