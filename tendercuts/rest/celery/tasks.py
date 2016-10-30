from .celery import app

from rest.lib.store.orders import OrderStore
from rest.lib.data_source.prod import TenderCuts
from rest.cache import redis

@app.task
def cache_addresses():
    store = OrderStore(TenderCuts(), redis.RedisCache())
    store.cache_addresses()