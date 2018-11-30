select
	product.entity_id, 
	meta_keyword.value keyword/is, 
	meta_description.value description,
	meta_title.value as title
from
catalog_product_entity product
left join catalog_product_entity_text meta_keyword on product.entity_id = meta_keyword.entity_id and meta_keyword.attribute_id = 83 and meta_keyword.store_id = 1
left join catalog_product_entity_varchar meta_description on product.entity_id = meta_description.entity_id and meta_description.attribute_id = 84 and meta_description.store_id = 1
left join catalog_product_entity_varchar meta_title on product.entity_id = meta_title.entity_id and meta_title.attribute_id = 82 and meta_title.store_id = 1





from __future__ import unicode_literals
    
from django.db import models
from django.conf import settings

from app.core.models.entity import EavAttribute

from app.core.models import SalesFlatOrder, SalesFlatOrderAddress, CoreStore

from app.core.models.product import CatalogProductEntity

# class CatalogProductEntityInt(models.Model):
#         value_id = models.AutoField(primary_key=True)
#         entity_type_id = models.IntegerField()
#         attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
#         store = models.ForeignKey('CoreStore', models.DO_NOTHING)
#         entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING)
#         value = models.IntegerField(blank=True, null=True)
    
#         class Meta:
#             managed = False
#             db_table = 'catalog_product_entity_int'
#             unique_together = (('entity', 'attribute', 'store'),)
#             app_label = "magento"

class CatalogProductEntityVarchar(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING,related_name='varchar')
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_varchar'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = "magento"

class CatalogProductEntityText(models.Model):
    value_id = models.AutoField(primary_key=True)
    entity_type_id = models.IntegerField()
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    entity = models.ForeignKey(CatalogProductEntity, models.DO_NOTHING,related_name='text')
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog_product_entity_text'
        unique_together = (('entity', 'attribute', 'store'),)
        app_label = "magento"

