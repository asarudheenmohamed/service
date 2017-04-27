# public function validateHash($password, $hash)
# {
#     $hashArr = explode(':', $hash);
#     switch (count($hashArr)) {
#         case 1:
#             return $this->hash($password) === $hash;
#         case 2:
#             return $this->hash($hashArr[1] . $password) === $hashArr[0];
#     }
#     Mage::throwException('Invalid hash.');
# }
from __future__ import unicode_literals

from django.db import models

class CustomerEntity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_type_id = models.SmallIntegerField()
    attribute_set_id = models.SmallIntegerField()
    # website = models.ForeignKey('CoreWebsite', models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    group_id = models.SmallIntegerField()
    increment_id = models.CharField(max_length=50, blank=True, null=True)
    store = models.ForeignKey(
        'CoreStore', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_active = models.SmallIntegerField()
    disable_auto_group_change = models.SmallIntegerField()
    vtiger_id = models.IntegerField(blank=True, null=True)
    vtiger_type = models.CharField(max_length=10, blank=True, null=True)
    vtiger_accountname = models.CharField(
        max_length=100, blank=True, null=True)
    vtiger_logintime = models.DateTimeField(blank=True, null=True)
    vtiger_logouttime = models.DateTimeField(blank=True, null=True)
    vtiger_numberlogin = models.IntegerField()
    vtiger_ip = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'customer_entity'
        unique_together = (('email', 'website'),)
        app_label = "magento"


# class RewardpointsCustomer(models.Model):
#     reward_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(
#         CustomerEntity, models.DO_NOTHING, related_name="reward_point")
#     point_balance = models.IntegerField()
#     holding_balance = models.IntegerField()
#     spent_balance = models.IntegerField()
#     is_notification = models.SmallIntegerField()
#     expire_notification = models.SmallIntegerField()
#     referal_id = models.IntegerField()
#     ip_adress = models.CharField(max_length=255, blank=True, null=True)
#     created_time = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'rewardpoints_customer'
#         app_label = "magento"


class CustomerEntityDatetime(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING, related_name="dates")
    value = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer_entity_datetime'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerEntityDecimal(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING, related_name="decimal")
    value = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'customer_entity_decimal'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerEntityInt(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING, related_name="ints")
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customer_entity_int'
        app_label = "magento"
        unique_together = (('entity', 'attribute'),)


class CustomerEntityText(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING, related_name="texts")
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'customer_entity_text'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"


class CustomerEntityVarchar(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING, related_name="varchars")
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_entity_varchar'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"

class MCreditBalance(models.Model):
    balance_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerEntity, models.DO_NOTHING, blank=True, null=True, related_name="store_credit")
    amount = models.FloatField(blank=True, null=True)
    is_subscribed = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm_credit_balance'
        app_label = "magento"

class MRewardsTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomerEntity, models.DO_NOTHING, related_name="reward_point")
    amount = models.IntegerField(blank=True, null=True)
    amount_used = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=255)
    is_expired = models.IntegerField()
    is_expiration_email_sent = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm_rewards_transaction'
        app_label = "magento"