"""Endpoint for the redis controller."""

import redis

from django.conf import settings


class RedisController(object):
    """Fetch the OTP from redis DB and create otp."""

    def __init__(self):
        """Intialized redis connection."""
        self.redis_db = redis.StrictRedis(**settings.REDIS)

    def set_key(self, key, value):
        """OTP key per value stored in redis DB.

        Args:
         key:key of stored row
         value:value of stored row

        This key value expire on 15 min.

        """
        redis_status = self.redis_db.setex(
            name=key,
            value=value,
            time=15 * 60  # 30 mins!
        )

        return redis_status

    def get_key(self, phone):
        """Fetch key based value in redis DB.

        Args:
         phone(int):user mobile number

        Returns:
            return a key object

        """
        obj = self.redis_db.get(phone)

        return obj
