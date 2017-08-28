# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from .product import CatalogProductEntity



# Old inventory model
class AitocCataloginventoryStockItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    website_id = models.IntegerField()
    product = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING)
    # stock = models.ForeignKey('CataloginventoryStock', models.DO_NOTHING)
    qty = models.DecimalField(max_digits=12, decimal_places=4)
    min_qty = models.DecimalField(max_digits=12, decimal_places=4)
    use_config_min_qty = models.IntegerField()
    is_qty_decimal = models.IntegerField()
    backorders = models.IntegerField()
    use_config_backorders = models.IntegerField()
    min_sale_qty = models.DecimalField(max_digits=12, decimal_places=4)
    use_config_min_sale_qty = models.IntegerField()
    max_sale_qty = models.DecimalField(max_digits=12, decimal_places=4)
    use_config_max_sale_qty = models.IntegerField()
    is_in_stock = models.IntegerField()
    low_stock_date = models.DateTimeField(blank=True, null=True)
    notify_stock_qty = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    use_config_notify_stock_qty = models.IntegerField()
    manage_stock = models.IntegerField()
    use_config_manage_stock = models.IntegerField()
    stock_status_changed_auto = models.SmallIntegerField()
    use_default_website_stock = models.IntegerField()
    use_config_qty_increments = models.IntegerField()
    qty_increments = models.DecimalField(max_digits=12, decimal_places=4)
    use_config_enable_qty_increments = models.IntegerField()
    enable_qty_increments = models.IntegerField()
    is_decimal_divided = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'aitoc_cataloginventory_stock_item'
        unique_together = (('product', 'stock', 'website_id'),)
        app_label = "magento"


class GraminventoryLatest(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    # product_id = models.IntegerField()
    product = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING)
    qty = models.FloatField(blank=True, null=True)
    scheduledqty = models.FloatField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    kg_qty = models.FloatField(blank=True, null=True)
    kg_expiring = models.FloatField(blank=True, null=True)
    kg_forecast = models.IntegerField(blank=True, null=True)
    gpu = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'graminventory_latest'
        app_label = "magento"
        # unique_together = (('product_id', 'store_id'),)
