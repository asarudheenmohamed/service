import magento
import pprint
import collections
import json



class OrderStore():

    def __init__(self, source, cache):
        self.source = source
        self.cache = cache

    def fetch(self):
        orders = self.source.fetch()
        return orders

    def cache_addresses(self):
        self.source.cache_addresses(self.cache)
