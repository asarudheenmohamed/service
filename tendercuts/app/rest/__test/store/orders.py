from store.orders import OrderStore
from data_source.mock import MockSource
from data_source.prod import TenderCuts

import googlemaps

def test_fetch():
    store = OrderStore(MockSource())
    orders = store.fetch()
#     print (orders)


#     store.source.dump()
