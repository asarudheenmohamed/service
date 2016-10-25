import magento
import pprint
import collections
import json



class OrderStore():

    def __init__(self, source):
        self.source = source

    def fetch(self):
        orders = self.source.fetch()
        return orders










