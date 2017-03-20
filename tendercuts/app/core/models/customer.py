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
    store = models.ForeignKey('CoreStore', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_active = models.SmallIntegerField()
    disable_auto_group_change = models.SmallIntegerField()
    vtiger_id = models.IntegerField(blank=True, null=True)
    vtiger_type = models.CharField(max_length=10, blank=True, null=True)
    vtiger_accountname = models.CharField(max_length=100, blank=True, null=True)
    vtiger_logintime = models.DateTimeField(blank=True, null=True)
    vtiger_logouttime = models.DateTimeField(blank=True, null=True)
    vtiger_numberlogin = models.IntegerField()
    vtiger_ip = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'customer_entity'
        unique_together = (('email', 'website'),)
        app_label = "magento"


class RewardpointsCustomer(models.Model):
    reward_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerEntity, models.DO_NOTHING, related_name="reward_point")
    point_balance = models.IntegerField()
    holding_balance = models.IntegerField()
    spent_balance = models.IntegerField()
    is_notification = models.SmallIntegerField()
    expire_notification = models.SmallIntegerField()
    referal_id = models.IntegerField()
    ip_adress = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rewardpoints_customer'
        app_label = "magento"


class CustomerEntityDatetime(models.Model):
    value_id = models.AutoField(primary_key=True)
    # entity_type = models.ForeignKey('EavEntityType', models.DO_NOTHING)
    attribute = models.ForeignKey('EavAttribute', models.DO_NOTHING)
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING)
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
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING)
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
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING)
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
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING)
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
    entity = models.ForeignKey(CustomerEntity, models.DO_NOTHING)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_entity_varchar'
        unique_together = (('entity', 'attribute'),)
        app_label = "magento"

import itertools
import sys
class Customer():
    """
    Bloody!

    There is no straight forward way to create from the models, because the EAV model in magento
    is fucking stupid!
    So all this monkey patching to handle this!
    """

    _MAPPING = {
        "firstname": ("CustomerEntityVarchar", 5),
        "lastname": ("CustomerEntityVarchar", 7),
        "mobile": ("CustomerEntityVarchar", 146),
    }

    def get_data(self, customer_id, attributes=None):
        if not attributes:
            attributes = list(self._MAPPING.keys())

        attributes = [self._MAPPING[attr] for attr in attributes]
        models_to_query = itertools.groupby(attributes, key=lambda x: x[0])

        customer = CustomerEntity.objects.filter(entity_id=customer_id)
        customer = customer[0]

        attributes_data = []
        for model_name, mappings in models_to_query:

            attribute_codes = [ mapping[1] for mapping in mappings ]
            model = getattr(sys.modules[__name__], model_name)

            attributes_data.extend(
                model.objects.filter(
                    attribute_id__in=attribute_codes,
                    entity_id=customer.entity_id).
                select_related('attribute'))

        data = {}
        for eav in attributes_data:
            data[eav.attribute.attribute_code] = eav.value

        data['email'] = customer.email
        data['reward_points'] = customer.reward_point.all()[0].point_balance

        return data

