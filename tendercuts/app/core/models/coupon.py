# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Salesrule(models.Model):
    rule_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    uses_per_customer = models.IntegerField()
    is_active = models.SmallIntegerField()
    conditions_serialized = models.TextField(blank=True, null=True)
    actions_serialized = models.TextField(blank=True, null=True)
    stop_rules_processing = models.SmallIntegerField()
    is_advanced = models.SmallIntegerField()
    product_ids = models.TextField(blank=True, null=True)
    sort_order = models.IntegerField()
    simple_action = models.CharField(max_length=32, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=4)
    discount_qty = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    discount_step = models.IntegerField()
    simple_free_shipping = models.SmallIntegerField()
    apply_to_shipping = models.SmallIntegerField()
    times_used = models.IntegerField()
    is_rss = models.SmallIntegerField()
    coupon_type = models.SmallIntegerField()
    use_auto_generation = models.SmallIntegerField()
    uses_per_coupon = models.IntegerField()

    class Meta:
        managed = False
        app_label = "magento"
        db_table = 'salesrule'


class SalesruleCoupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    rule = models.ForeignKey('Salesrule', models.DO_NOTHING)
    code = models.CharField(unique=True, max_length=255, blank=True, null=True)
    usage_limit = models.IntegerField(blank=True, null=True)
    usage_per_customer = models.IntegerField(blank=True, null=True)
    times_used = models.IntegerField()
    expiration_date = models.DateTimeField(blank=True, null=True)
    is_primary = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    type = models.SmallIntegerField(blank=True, null=True)
    is_popup = models.IntegerField(blank=True, null=True)
    user_ip = models.CharField(max_length=20, blank=True, null=True)
    popup_cookie_id = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesrule_coupon'
        app_label = "magento"
        unique_together = (('rule', 'is_primary'),)