import magento
import pprint
import collections
import json

from ..models.magento import ShippingAddress, SalesOrder


class MockSource():

    def fetch(self):
        data = json.load(open('/Users/varunprasad/MyProjects/workspaces/xyz/geo/data_source/dump.dat', 'r'))

        orders = []
        for ord_dict in data:
            shipping = ShippingAddress(ord_dict.pop('shipping_address'))
            order = SalesOrder(ord_dict, shipping)
            orders.append(order)

        return orders


