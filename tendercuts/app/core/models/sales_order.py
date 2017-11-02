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
from django.utils import timezone
from .driver_models import DriverManagement
from .store import CoreStore
import datetime
import dateutil.parser
import pytz
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SalesFlatOrder(models.Model):
    entity_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    protect_code = models.CharField(max_length=255, blank=True, null=True)
    shipping_description = models.CharField(
        max_length=255, blank=True, null=True)
    is_virtual = models.SmallIntegerField(blank=True, null=True)
    base_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_grand_total = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_subtotal = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_subtotal_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_subtotal_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_subtotal_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_to_global_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_to_order_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_invoiced_cost = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_offline_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_online_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_paid = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_qty_ordered = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    grand_total = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    store_to_base_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    store_to_order_rate = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    subtotal_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    subtotal_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    subtotal_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_offline_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_online_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_paid = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_qty_ordered = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    can_ship_partially = models.SmallIntegerField(blank=True, null=True)
    can_ship_partially_item = models.SmallIntegerField(blank=True, null=True)
    customer_is_guest = models.SmallIntegerField(blank=True, null=True)
    customer_note_notify = models.SmallIntegerField(blank=True, null=True)
    billing_address_id = models.IntegerField(blank=True, null=True)
    customer_group_id = models.SmallIntegerField(blank=True, null=True)
    edit_increment = models.IntegerField(blank=True, null=True)
    email_sent = models.SmallIntegerField(blank=True, null=True)
    forced_shipment_with_invoice = models.SmallIntegerField(
        blank=True, null=True)
    payment_auth_expiration = models.IntegerField(blank=True, null=True)
    quote_address_id = models.IntegerField(blank=True, null=True)
    quote_id = models.IntegerField(blank=True, null=True)
    adjustment_negative = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    adjustment_positive = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_adjustment_negative = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_adjustment_positive = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_subtotal_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_due = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    payment_authorization_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    subtotal_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_due = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customer_dob = models.DateTimeField(blank=True, null=True)
    increment_id = models.CharField(
        unique=True, max_length=50, blank=True, null=True)
    applied_rule_ids = models.CharField(max_length=255, blank=True, null=True)
    base_currency_code = models.CharField(max_length=3, blank=True, null=True)
    customer_email = models.CharField(max_length=255, blank=True, null=True)
    customer_firstname = models.CharField(
        max_length=255, blank=True, null=True)
    customer_lastname = models.CharField(max_length=255, blank=True, null=True)
    customer_middlename = models.CharField(
        max_length=255, blank=True, null=True)
    customer_prefix = models.CharField(max_length=255, blank=True, null=True)
    customer_suffix = models.CharField(max_length=255, blank=True, null=True)
    customer_taxvat = models.CharField(max_length=255, blank=True, null=True)
    discount_description = models.CharField(
        max_length=255, blank=True, null=True)
    ext_customer_id = models.CharField(max_length=255, blank=True, null=True)
    ext_order_id = models.CharField(max_length=255, blank=True, null=True)
    global_currency_code = models.CharField(
        max_length=3, blank=True, null=True)
    hold_before_state = models.CharField(max_length=255, blank=True, null=True)
    hold_before_status = models.CharField(
        max_length=255, blank=True, null=True)
    order_currency_code = models.CharField(
        max_length=255, blank=True, null=True)
    original_increment_id = models.CharField(
        max_length=50, blank=True, null=True)
    relation_child_id = models.CharField(max_length=32, blank=True, null=True)
    relation_child_real_id = models.CharField(
        max_length=32, blank=True, null=True)
    relation_parent_id = models.CharField(max_length=32, blank=True, null=True)
    relation_parent_real_id = models.CharField(
        max_length=32, blank=True, null=True)
    remote_ip = models.TextField(blank=True, null=True)
    shipping_method = models.CharField(max_length=255, blank=True, null=True)
    store_currency_code = models.CharField(max_length=3, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    x_forwarded_for = models.CharField(max_length=255, blank=True, null=True)
    customer_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total_item_count = models.SmallIntegerField()
    customer_gender = models.IntegerField(blank=True, null=True)
    hidden_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_hidden_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_hidden_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_hidden_tax_amnt = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    hidden_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_hidden_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    hidden_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_hidden_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_incl_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    coupon_rule_name = models.CharField(max_length=255, blank=True, null=True)
    paypal_ipn_customer_notified = models.IntegerField(blank=True, null=True)
    gift_message_id = models.IntegerField(blank=True, null=True)
    base_customer_balance_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customer_balance_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customer_balance_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customer_balance_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customer_balance_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customer_balance_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    bs_customer_bal_total_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customer_bal_total_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_cards = models.TextField(blank=True, null=True)
    base_gift_cards_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_cards_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_gift_cards_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_cards_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_gift_cards_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_cards_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_id = models.IntegerField(blank=True, null=True)
    gw_allow_gift_receipt = models.IntegerField(blank=True, null=True)
    gw_add_card = models.IntegerField(blank=True, null=True)
    gw_base_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
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
    gw_base_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_base_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_base_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_tax_amount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_base_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_base_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_base_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_base_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_tax_amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_base_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_items_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_base_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_card_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    reward_points_balance = models.IntegerField(blank=True, null=True)
    base_reward_currency_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    reward_currency_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_rwrd_crrncy_amt_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    rwrd_currency_amount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_rwrd_crrncy_amnt_refnded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    rwrd_crrncy_amnt_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    reward_points_balance_refund = models.IntegerField(blank=True, null=True)
    reward_points_balance_refunded = models.IntegerField(blank=True, null=True)
    reward_salesrule_points = models.IntegerField(blank=True, null=True)
    shipping_progress = models.IntegerField(blank=True, null=True)
    rewardpoints_earn = models.IntegerField()
    rewardpoints_spent = models.IntegerField()
    rewardpoints_base_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_base_amount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_amount = models.DecimalField(max_digits=12, decimal_places=4)
    rewardpoints_referal_earn = models.IntegerField()
    rewardpoints_invited_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_invited_base_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_refer_customer_id = models.IntegerField()
    vtiger_id = models.IntegerField(blank=True, null=True)
    location_id = models.IntegerField()
    custom_status = models.CharField(max_length=50)
    mail_send = models.IntegerField()
    cordinates = models.CharField(max_length=20)
    trip_id = models.CharField(max_length=200)
    order_now = models.IntegerField()

    customercredit_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customercredit_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customercredit_discount_for_shipping = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customercredit_discount_for_shipping = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customercredit_hidden_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customercredit_hidden_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_customercredit_shipping_hidden_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customercredit_shipping_hidden_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)

    # scheduled order related data
    medium = models.IntegerField(blank=True, null=True)
    os = models.IntegerField(blank=True, null=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    scheduled_slot = models.IntegerField(blank=True, null=True)
    deliverytype = models.IntegerField(blank=True, null=True)

    splitted = models.IntegerField(blank=True, null=True)
    splittedfrom = models.CharField(max_length=255, blank=True, null=True)
    splittedto = models.CharField(max_length=255, blank=True, null=True)
    payment_recieved = models.IntegerField(blank=True, null=True)

    store = models.ForeignKey(
        CoreStore, models.DO_NOTHING, blank=True, null=True)
    store_id = models.IntegerField()
    # removing it till a time comes to integrate this
    # customer = models.ForeignKey('CustomerEntity', models.DO_NOTHING, blank=True, null=True)
    customer_id = models.IntegerField()

    # Replace these ID fields with models
    driver_id = models.IntegerField()
    # shipping_address_id = models.IntegerField(blank=True, null=True)

    # to_field by default points to the primay key
    # Database Representation

    # Behind the scenes, Django appends "_id" to the field name to create its database column
    # name, can be changed by db_colum
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.to_field
    # driver = models.ForeignKey(DriverManagement, models.DO_NOTHING, blank=True, null=True)

    # shipping_address = models.ForeignKey(SalesFlatOrderAddress, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_flat_order'
        app_label = "magento"

    @property
    def is_cod(self):
        return self.payment.all()[0].method == "cashondelivery"

    @property
    def is_payu(self):
        try:
            return self.payment.all()[0].method == "payubiz"
        except:
            # incase of buggy orders like 00000086
            return False

    @property
    def is_paytm(self):
        return self.payment.all()[0].method == "paytm"

    def time_elapsed(self):
        return timezone.now() - self.created_at

    def compute_delivery_time(self):
        """
        TODO needs optimization
        """
        SLOTS = {52: "7:00 - 9:00",
                 53: "9:00 - 11:00",
                 54: "11:00 - 13:00",
                 55: "17:00 - 19:00",
                 56: "19:00 - 21:00"}

        promised_time = None
        tz = pytz.timezone('Asia/Kolkata')

        if self.deliverytype == 1:
            promised_time = self.created_at + datetime.timedelta(minutes=120)
            promised_time = promised_time.astimezone(tz)

        elif self.deliverytype == 2:
            date_obj = self.scheduled_date
            timetext = self.scheduled_slot
            timetext = SLOTS[timetext].split("-")
            if len(timetext) == 2:
                timetext = timetext[1]
            else:
                timetext = "00"

            logger.debug(
                "Formatting {}: {} to text".format(
                    date_obj, timetext))
            try:
                promised_time = dateutil.parser.parse(
                    "{} {}".format(date_obj, timetext))
            except Exception as e:
                logger.info("Conversion to date faile")
                promised_time = None

        return promised_time

    @property
    def promised_delivery_time(self):
        promised_time = self.compute_delivery_time()
        return format(
            promised_time, '%b %d, %a %I:%M %p') if promised_time else ""

    @property
    def promised_delivery_time_dt(self):
        promised_time = self.compute_delivery_time()
        return promised_time if promised_time else ""


class SalesFlatOrderItem(models.Model):
    # store = models.ForeignKey('CoreStore', models.DO_NOTHING, blank=True, null=True)
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        SalesFlatOrder, models.DO_NOTHING, related_name="items")
    parent_item_id = models.IntegerField(blank=True, null=True)
    quote_item_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    product_id = models.IntegerField(blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    product_options = models.TextField(blank=True, null=True)
    weight = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    is_virtual = models.SmallIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    applied_rule_ids = models.TextField(blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    free_shipping = models.SmallIntegerField()
    is_qty_decimal = models.SmallIntegerField()
    no_discount = models.SmallIntegerField()
    qty_backordered = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    qty_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    qty_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    qty_ordered = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    qty_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    qty_shipped = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_cost = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    base_price = models.DecimalField(max_digits=12, decimal_places=4)
    original_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_original_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_percent = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_percent = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    row_total = models.DecimalField(max_digits=12, decimal_places=4)
    base_row_total = models.DecimalField(max_digits=12, decimal_places=4)
    row_invoiced = models.DecimalField(max_digits=12, decimal_places=4)
    base_row_invoiced = models.DecimalField(max_digits=12, decimal_places=4)
    row_weight = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_before_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_before_discount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    ext_order_item_id = models.CharField(max_length=255, blank=True, null=True)
    locked_do_invoice = models.SmallIntegerField(blank=True, null=True)
    locked_do_ship = models.SmallIntegerField(blank=True, null=True)
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
    hidden_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_hidden_tax_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    hidden_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_hidden_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    is_nominal = models.IntegerField()
    tax_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    hidden_tax_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_tax_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    discount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_discount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gift_message_id = models.IntegerField(blank=True, null=True)
    gift_message_available = models.IntegerField(blank=True, null=True)
    base_weee_tax_applied_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_applied_row_amnt = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_applied_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_applied_row_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_applied = models.TextField(blank=True, null=True)
    weee_tax_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    weee_tax_row_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_weee_tax_row_disposition = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    event_id = models.IntegerField(blank=True, null=True)
    giftregistry_item_id = models.IntegerField(blank=True, null=True)
    gw_id = models.IntegerField(blank=True, null=True)
    gw_base_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_tax_amount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount_invoiced = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_price_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_base_tax_amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    gw_tax_amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    qty_returned = models.DecimalField(max_digits=12, decimal_places=4)
    rewardpoints_earn = models.IntegerField()
    rewardpoints_spent = models.IntegerField()
    rewardpoints_base_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_referal_earn = models.IntegerField()
    rewardpoints_invited_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    rewardpoints_invited_base_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    item_comment = models.TextField(blank=True, null=True)
    customercredit_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    base_customercredit_discount = models.DecimalField(
        max_digits=12, decimal_places=4)
    base_customercredit_hidden_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    customercredit_hidden_tax = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    deliverydate = models.DateTimeField(blank=True, null=True)
    deliveryslot = models.IntegerField(blank=True, null=True)
    promisedeliverytime = models.CharField(max_length=255, blank=True, null=True)
    deliverytype = models.IntegerField(blank=True, null=True)
    grams = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_flat_order_item'
        app_label = "magento"


class SalesFlatOrderAddress(models.Model):
    entity_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(SalesFlatOrder, models.DO_NOTHING,
                               blank=True, null=True, related_name="shipping_address")
    customer_address_id = models.IntegerField(blank=True, null=True)
    quote_address_id = models.IntegerField(blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.CharField(max_length=2, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    address_type = models.CharField(max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=255, blank=True, null=True)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    suffix = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    vat_id = models.TextField(blank=True, null=True)
    vat_is_valid = models.SmallIntegerField(blank=True, null=True)
    vat_request_id = models.TextField(blank=True, null=True)
    vat_request_date = models.TextField(blank=True, null=True)
    vat_request_success = models.SmallIntegerField(blank=True, null=True)
    giftregistry_item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_flat_order_address'
        app_label = "magento"


class SalesFlatOrderPayment(models.Model):
    entity_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(
        SalesFlatOrder, models.DO_NOTHING, related_name='payment')
    base_shipping_captured = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_captured = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_paid = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    amount_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_authorized = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_paid_online = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_refunded_online = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    amount_paid = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    amount_authorized = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_ordered = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_shipping_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_refunded = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    amount_ordered = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_amount_canceled = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    quote_payment_id = models.IntegerField(blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    cc_exp_month = models.CharField(max_length=255, blank=True, null=True)
    cc_ss_start_year = models.CharField(max_length=255, blank=True, null=True)
    echeck_bank_name = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=255, blank=True, null=True)
    cc_debug_request_body = models.CharField(
        max_length=255, blank=True, null=True)
    cc_secure_verify = models.CharField(max_length=255, blank=True, null=True)
    protection_eligibility = models.CharField(
        max_length=255, blank=True, null=True)
    cc_approval = models.CharField(max_length=255, blank=True, null=True)
    cc_last4 = models.CharField(max_length=255, blank=True, null=True)
    cc_status_description = models.CharField(
        max_length=255, blank=True, null=True)
    echeck_type = models.CharField(max_length=255, blank=True, null=True)
    cc_debug_response_serialized = models.CharField(
        max_length=255, blank=True, null=True)
    cc_ss_start_month = models.CharField(max_length=255, blank=True, null=True)
    echeck_account_type = models.CharField(
        max_length=255, blank=True, null=True)
    last_trans_id = models.CharField(max_length=255, blank=True, null=True)
    cc_cid_status = models.CharField(max_length=255, blank=True, null=True)
    cc_owner = models.CharField(max_length=255, blank=True, null=True)
    cc_type = models.CharField(max_length=255, blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=True, null=True)
    cc_exp_year = models.CharField(max_length=255, blank=True, null=True)
    cc_status = models.CharField(max_length=255, blank=True, null=True)
    echeck_routing_number = models.CharField(
        max_length=255, blank=True, null=True)
    account_status = models.CharField(max_length=255, blank=True, null=True)
    anet_trans_method = models.CharField(max_length=255, blank=True, null=True)
    cc_debug_response_body = models.CharField(
        max_length=255, blank=True, null=True)
    cc_ss_issue = models.CharField(max_length=255, blank=True, null=True)
    echeck_account_name = models.CharField(
        max_length=255, blank=True, null=True)
    cc_avs_status = models.CharField(max_length=255, blank=True, null=True)
    cc_number_enc = models.CharField(max_length=255, blank=True, null=True)
    cc_trans_id = models.CharField(max_length=255, blank=True, null=True)
    paybox_request_number = models.CharField(
        max_length=255, blank=True, null=True)
    address_status = models.CharField(max_length=255, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    cybersource_token = models.CharField(max_length=255, blank=True, null=True)
    flo2cash_account_id = models.CharField(
        max_length=255, blank=True, null=True)
    ideal_issuer_id = models.CharField(max_length=255, blank=True, null=True)
    ideal_issuer_title = models.CharField(
        max_length=255, blank=True, null=True)
    ideal_transaction_checked = models.IntegerField(blank=True, null=True)
    paybox_question_number = models.CharField(
        max_length=255, blank=True, null=True)
    ccforpos_ref_no = models.CharField(max_length=255)
    cp1forpos_ref_no = models.CharField(max_length=255)
    cp2forpos_ref_no = models.CharField(max_length=255)
    codforpos_ref_no = models.CharField(max_length=255)
    cashforpos_ref_no = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sales_flat_order_payment'
        app_label = "magento"


class SalesFlatOrderGrid(models.Model):
    entity = models.OneToOneField(
        SalesFlatOrder, models.DO_NOTHING, primary_key=True, related_name="grid")
    status = models.CharField(max_length=32, blank=True, null=True)
    # store = models.ForeignKey('CoreStore', models.DO_NOTHING, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    # customer = models.ForeignKey('CustomerEntity', models.DO_NOTHING, blank=True, null=True)
    base_grand_total = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    base_total_paid = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    grand_total = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    total_paid = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True)
    increment_id = models.CharField(
        unique=True, max_length=50, blank=True, null=True)
    base_currency_code = models.CharField(max_length=3, blank=True, null=True)
    order_currency_code = models.CharField(
        max_length=255, blank=True, null=True)
    shipping_name = models.CharField(max_length=255, blank=True, null=True)
    billing_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vtiger_id = models.IntegerField(blank=True, null=True)
    #driver = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_flat_order_grid'
        app_label = "magento"


class Mwddate(models.Model):
    ddate_id = models.AutoField(primary_key=True)
    ddate = models.DateField(blank=True, null=True)
    dtime = models.CharField(max_length=50)
    ampm = models.IntegerField()
    holiday = models.IntegerField(blank=True, null=True)
    ordered = models.IntegerField()
    dtimetext = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mwddate'
        app_label = 'magento'


class MwddateStore(models.Model):
    ddate_store_id = models.AutoField(primary_key=True)
    increment_id = models.CharField(max_length=50)
    # ddate_id = models.IntegerField()
    ddate = models.OneToOneField(
        "Mwddate", models.DO_NOTHING, related_name="schedule_date")
    ddate_comment = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=50, blank=True, null=True)
    #sales_order_id = models.IntegerField()
    order = models.OneToOneField(
        SalesFlatOrder, models.DO_NOTHING,
        related_name="schedule",
        db_column='sales_order_id',
        to_field='entity_id')

    class Meta:
        managed = False
        db_table = 'mwddate_store'
        app_label = 'magento'
