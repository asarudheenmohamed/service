import redis
import functools

def memoize(func):
    client = redis.Redis()
    client.flushall()

    @functools.wraps()
    def func_wrapper(key, value):
        pass



