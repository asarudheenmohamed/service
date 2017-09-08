"""Endpoint for the Set Cache value and Get Cache value."""
from django.core.cache import cache
from django.conf import settings


def set_key(key, value, time, version=settings.CACHE_DEFAULT_VERSION):
    """Sets a value to the cache.

    Params:
     key(str): Location of the value
     value(list): Value to cache
     time: Number of seconds to hold value in cache
     version(int): Version of keys

    """
    cache.set(key, value, time, version=version)


def get_key(key, version=settings.CACHE_DEFAULT_VERSION):
    """Retrieves a value from the cache.

    Params:
    key(str): Location of the value
    version(int): Version of keys

    Returns:
        Value that was cached

    """

    cache_obj = cache.get(key, version=version)

    return cache_obj
