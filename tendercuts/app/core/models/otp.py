# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    def redis_save(redis_conn, model, prefix="FORGOT_OTP"):
        redis_conn.setex(
            name="{}:{}".format(prefix, model.mobile),
            value=model.otp,
            time = 30 * 60 # 30 mins!
        )
    
    @staticmethod
    def redis_get(redis_conn, phone, prefix="FORGOT_OTP"):
        otp = redis_conn.get("{}:{}".format(prefix, phone))
        if otp is None:
            return otp

        return OtpList(mobile=phone, otp=otp)


