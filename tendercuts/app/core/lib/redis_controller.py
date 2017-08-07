"""Endpoint for the redis controll."""
import logging

import redis
from .. import lib, models
from django.conf import settings


class RedisController:
    """Fetch the OTP from redis DB and create otp."""

    def __init__(self, log=None):
        """Intialized the logger and redis connection."""
        self.redis_db = redis.StrictRedis(**settings.REDIS)

    def redis_save(self, model, prefix):
        """OTP stored in redis DB.

        Args:
         redis_conn:redis connection
         model(obj):otp object
         prefix(str):otp types are FORGOT,SIGNUP,LOGIN

        1.this otp expired on 30 min.
        """
        name = "{}:{}".format(prefix, model.mobile)
        redis_status = self.redis_db.setex(
            name=name,
            value=model.otp,
            time=30 * 60  # 30 mins!
        )
        return redis_status

    def set(self, key, value):
        """OTP key per value stored in redis DB.

        Args:
         key:key of stored row
         value:value of stored row

        1.this key value expire on 15 min.
        """
        redis_status = self.redis_db.setex(
            name=key,
            value=value,
            time=15 * 60  # 30 mins!
        )
        return redis_status

    def redis_get(self, phone, prefix):
        """OTP fetch in redis DB.

        Args:
         redis_conn:redis connection

         prefix(str):otp types are FORGOT,SIGNUP,LOGIN
         phone(int):user mobile number

        Returns:
            return a OTP object

        """
        name = "{}:{}".format(prefix, phone)
        otp = self.redis_db.get(name)
        if otp is None:
            return otp

        return models.OtpList(mobile=phone, otp=otp)

    def get(self, phone):
        """Fetch key based value in redis DB.

        Args:
         phone(int):user mobile number

        Returns:
            return a key object

        """
        obj = self.redis_db.get(phone)
        return obj
