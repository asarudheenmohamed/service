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


class SalesFlatQuote(models.Model):
    entity_id = models.AutoField(primary_key=True)
    store = models.ForeignKey('CoreStore', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    converted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.SmallIntegerField(blank=True, null=True)
    is_virtual = models.SmallIntegerField(blank=True, null=True)
    is_multi_shipping = models.SmallIntegerField(blank=True, null=True)
    items_count = models.IntegerField(blank=True, null=True)
    items_qty = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    orig_order_id = models.IntegerField(blank=True, null=True)
    store_to_base_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    store_to_quote_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_currency_code = models.CharField(
        max_length=255, blank=True, null=True)
    store_currency_code = models.CharField(
        max_length=255, blank=True, null=True)
    quote_currency_code = models.CharField(
        max_length=255, blank=True, null=True)
    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    base_grand_total = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    checkout_method = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    customer_tax_class_id = models.IntegerField(blank=True, null=True)
    customer_group_id = models.IntegerField(blank=True, null=True)
    customer_email = models.CharField(max_length=255, blank=True, null=True)
    customer_prefix = models.CharField(max_length=40, blank=True, null=True)
    customer_firstname = models.CharField(
        max_length=255, blank=True, null=True)
    customer_middlename = models.CharField(
        max_length=40, blank=True, null=True)
    customer_lastname = models.CharField(max_length=255, blank=True, null=True)
    customer_suffix = models.CharField(max_length=40, blank=True, null=True)
    customer_dob = models.DateTimeField(blank=True, null=True)
    customer_note = models.CharField(max_length=255, blank=True, null=True)
    customer_note_notify = models.SmallIntegerField(blank=True, null=True)
    customer_is_guest = models.SmallIntegerField(blank=True, null=True)
    remote_ip = models.CharField(max_length=255, blank=True, null=True)
    applied_rule_ids = models.CharField(max_length=255, blank=True, null=True)
    reserved_order_id = models.CharField(max_length=64, blank=True, null=True)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    global_currency_code = models.CharField(
        max_length=255, blank=True, null=True)
    base_to_global_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_to_quote_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customer_taxvat = models.CharField(max_length=255, blank=True, null=True)
    customer_mobile = models.CharField(max_length=255, blank=True, null=True)
    customer_gender = models.CharField(max_length=255, blank=True, null=True)
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    base_subtotal = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    subtotal_with_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_subtotal_with_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    is_changed = models.IntegerField(blank=True, null=True)
    trigger_recollect = models.SmallIntegerField()
    ext_shipping_info = models.TextField(blank=True, null=True)
    gift_message_id = models.IntegerField(blank=True, null=True)
    is_persistent = models.SmallIntegerField(blank=True, null=True)
    customer_balance_amount_used = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customer_bal_amount_used = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    use_customer_balance = models.IntegerField(blank=True, null=True)
    gift_cards = models.TextField(blank=True, null=True)
    gift_cards_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_gift_cards_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_cards_amount_used = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_gift_cards_amount_used = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_id = models.IntegerField(blank=True, null=True)
    gw_allow_gift_receipt = models.IntegerField(blank=True, null=True)
    gw_add_card = models.IntegerField(blank=True, null=True)
    gw_base_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    gw_items_base_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_base_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    use_reward_points = models.IntegerField(blank=True, null=True)
    reward_points_balance = models.IntegerField(blank=True, null=True)
    base_reward_currency_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    reward_currency_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    vtiger_id = models.IntegerField(blank=True, null=True)
    vtiger_currency_rate = models.DecimalField(max_digits=12, decimal_places=4)
    use_credit = models.IntegerField()
    base_credit_amount_used = models.DecimalField(
        max_digits=12, decimal_places=4)
    credit_amount_used = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'sales_flat_quote'
        app_label = "magento"


class SalesFlatQuoteItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    quote = models.ForeignKey(
        'SalesFlatQuote',
        models.DO_NOTHING,
        related_name='quote_item')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    product = models.ForeignKey(
        'CatalogProductEntity',
        models.DO_NOTHING,
        blank=True,
        null=True)
    store = models.ForeignKey(
        'CoreStore',
        models.DO_NOTHING,
        blank=True,
        null=True)
    parent_item = models.ForeignKey(
        'self', models.DO_NOTHING, blank=True, null=True)
    is_virtual = models.SmallIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    applied_rule_ids = models.TextField(blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    free_shipping = models.SmallIntegerField()
    is_qty_decimal = models.SmallIntegerField(blank=True, null=True)
    no_discount = models.SmallIntegerField(blank=True, null=True)
    weight = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    qty = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    base_price = models.DecimalField(max_digits=12, decimal_places=4)
    custom_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_percent = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_percent = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    row_total = models.DecimalField(max_digits=12, decimal_places=4)
    base_row_total = models.DecimalField(max_digits=12, decimal_places=4)
    row_total_with_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    row_weight = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    base_tax_before_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_before_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    original_custom_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    redirect_url = models.CharField(max_length=255, blank=True, null=True)
    base_cost = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    price_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_price_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    row_total_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_row_total_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    hidden_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_hidden_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_message_id = models.IntegerField(blank=True, null=True)
    weee_tax_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_row_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_row_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_applied = models.TextField(blank=True, null=True)
    weee_tax_applied_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_applied_row_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_applied_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_applied_row_amnt = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    giftregistry_item_id = models.IntegerField(blank=True, null=True)
    gw_id = models.IntegerField(blank=True, null=True)
    gw_base_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        blank=True,
        null=True)
    gw_base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    vtiger_list_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    deliverydate = models.DateTimeField(blank=True, null=True)
    deliveryslot = models.IntegerField(blank=True, null=True)
    promisedeliverytime = models.CharField(
        max_length=255, blank=True, null=True)
    deliverytype = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_flat_quote_item'
        app_label = "magento"
