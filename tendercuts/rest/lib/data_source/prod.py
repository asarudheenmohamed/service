import magento
import pprint
import collections
import json
import logging

from rest.models.point import Order
from rest.constants import REDIS

class TenderCuts():

    class MagentoOrder():
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.shipping = None
            self.lat , self.long = None, None

        def as_dict(self):
            self.__dict__['shipping_address'] = self.shipping
            return self.__dict__


    def __init__(self, log=None):
        self._api = magento.MagentoAPI(
                "www.tendercuts.in",
                port=443,
                api_user="admin",
                api_key="Tendercuts123!",
                proto="https",
                path="/index.php/api/xmlrpc/")

        import googlemaps
        self.gapi = googlemaps.Client(key='AIzaSyCQK2O4AMogjO323B-6btf9f2krVWST3bU')
        self.log = log or logging.getLogger()


    def _fetch(self):
        from_ = '2016-10-29 08:00:41',
        to_ = '2016-10-29 19:00:43'
        orders = self._api.sales_order.list({
                "created_at": {
                    "from": from_,
                    "to": to_
                    },
                "status": {"in": ['processing']}
             })

        self.log.info("Got {} orders for the time period {} - {}".format(
            len(orders), from_ , to_))

        increment_ids = {}
        for ord in orders:
            ord = self.__class__.MagentoOrder(**ord)
            increment_ids[ord.increment_id] = ord

        pending_orders = []
        for inc_id, ord in increment_ids.items():
            info = self._api.sales_order.info({'increment_id': inc_id})
            ord.shipping = info['shipping_address']
            pending_orders.append(ord)

        return pending_orders

    def fetch(self):
        orders = self._fetch()

        pending_orders = []
        for ord in orders:
            add = ord.shipping['street']
            add = add.split('\n')[0]
            resp = self.gapi.geocode(add,
                    components={'postal_code': ord.shipping['postcode']})
            print (ord.shipping)
            try:
                data = resp[0]['geometry']['location']
                ord.lat = data['lat']
                ord.long = data['lng']
            except Exception as e:
                self.log.exception("Unable to resolve {}".format(ord.shipping))
                pass

            print ("======================")

            pending_orders.append(Order(ord.order_id, ord.lat, ord.long))

        return pending_orders

    def cache_addresses(self, cache):
        orders = self._fetch()

        for ord in orders:
            print (ord)
            add = ord.shipping['street']
            add = add.split('\n')[0]
            resp = self.gapi.geocode(add)
#                     components={'postal_code': ord.shipping['postcode']})

            try:
                data = resp[0]['geometry']['location']
                ord.lat = data['lat']
                ord.long = data['lng']

                key = "{}:{}".format(
                        REDIS.SHIPPING_ADRRESS.value,
                        ord.shipping_address_id)

                value = "{},{}".format(ord.lat, ord.long)
                cache.set(key, value)
            except Exception as e:
                self.log.exception("Unable to resolve {}".format(ord.shipping))

    def dump(self):
        orders = self.fetch()

        orders = [ord.as_dict() for ord in orders]

        json.dump(orders, open("dump.dat", "w"))








