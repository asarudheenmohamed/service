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


class OtpList(models.Model):
    mobile = models.CharField(max_length=12, blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otp_list'
        app_label = "magento"

    @staticmethod
    def redis_save(redis_conn, model, type_=None, prefix="FORGOT_OTP"):
        """OTP stored in redis DB.
        Args:
         redis_conn:redis connection
         model(obj):otp object
         type_(int):otp types are forgot otp=1 or signup otp=2

        1.this otp expired on 30 min.
        """
        if type_ is None:
            name = "{}:{}".format(prefix, model.mobile)
        else:
            name = "{}:{}:{}".format(prefix, model.mobile, type_)
        redis_conn.setex(
            name=name,
            value=model.otp,
            time=30 * 60  # 30 mins!
        )

    @staticmethod
    def redis_key_value_save(redis_conn, key, value):
        """OTP key per value stored in redis DB.

        Args:
         redis_conn:redis connection
         key:key of stored row
         value:value of stored row

        1.this key value expire on 15 min.
        """
        redis_conn.setex(
            name=key,
            value=value,
            time=15 * 60  # 30 mins!
        )

    @staticmethod
    def redis_get(redis_conn, phone, type_=None, prefix="FORGOT_OTP"):
        """OTP fetch in redis DB.
        Args:
         redis_conn:redis connection
         model(obj):otp object
         type_(int):otp types forgot otp=1 or signup otp=2
         phone(int):user mobile number

        Returns:
            return a OTP object

        """
        if type_ is None:
            name = "{}:{}".format(prefix, phone)
        else:
            name = "{}:{}:{}".format(prefix, phone, type_)
        otp = redis_conn.get(name)
        if otp is None:
            return otp

        return OtpList(mobile=phone, otp=otp)

    @staticmethod
    def redis_key_based_get(redis_conn, phone):
        """fetch key based value in redis DB.
        Args:
         redis_conn:redis connection
         phone(int):user mobile number

        Returns:
            return a key object

        """
        obj = redis_conn.get(phone)

        return obj
