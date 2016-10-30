import redis
import functools
import logging

# Not used
def cache_value(func, prefix=""):

    @functools.wraps
    def wrapped_func(*args, **kwargs):
        key, value = func(*args, **kwargs)

        key = "{}:{}".format(prefix, key)
        RedisCache().set(key, value)

        return key, value

    return wrapped_func


class RedisCache:

    def __init__(self, log=None):
        self._client = redis.Redis()
        self.log = log or logging.getLogger()

    def set(self, key, value):
        self.log.debug("Setting {} for {}".format(key, value))
        self._client.set(key, value)

    def get(self, key):
        value = self._client.get(key)

        if not value:
            return None

        return value.decode('utf-8')



