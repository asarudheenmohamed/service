from django.shortcuts import render
# from rest.lib.models.point import DistributionCenter
from rest.lib.engine import Engine

# Create your views here.

from django.http import HttpResponse
from rest.models.point import Order
import rest.lib.store
from rest_framework.views import APIView
from rest_framework.response import Response
from rest.lib.store.orders import OrderStore
from rest.lib.data_source.mock import MockSource
from rest.lib.data_source.prod import TenderCuts

import random
import time
import uuid
import json

def make_orders():
    orders = []
    coords = [
            (12.92908, 77.62187900000004),
            (12.930011939588985, 77.62474358081818),
            (12.931444516664055, 77.62464702129364),
            (12.931323157570429, 77.62162902432863),
#             (12.931392232973792, 77.62230813503265),
            (12.934325331065297, 77.62361705303192),
            (12.932113746931863, 77.62368679046631),
            (12.924192664232187, 77.61876225471497),
            (12.925682788093471, 77.61667549610138),
            (12.923371785183274, 77.61576890945435),
            (12.921745704705058, 77.62393355369568),
            (12.92409332232521, 77.62592375278473),
            (12.923936466602155, 77.63002753257751),
            (12.933274438921474, 77.61231422424316),
            (12.932667951888742, 77.6069712638855),
            (12.930304729732805, 77.60546922683716),
            (12.936787852031962, 77.6063060760498),
            (12.935261196461985, 77.60431051254272),
            (12.942183354375915, 77.61360168457031),
            (12.94226700465603, 77.61164903640747),
            (12.944044566473055, 77.60701417922974),
            (12.94458828873272, 77.61664867401123),
            (12.940928596806609, 77.62276411056519),
            (12.945529343687165, 77.62130498886108),
            (12.946512219512973, 77.62368679046631),
            (12.942957118395979, 77.62913703918457),
            (12.940426692010892, 77.62900829315186),
        ]

#     for order_id, cord in enumerate(coords):
#         model = Order.from_dict({'id': order_id,
#                               'lat': cord[0],
#                               'long': cord[1]})
#         orders.append(model)

    for _ in range(1, 10):
        lat = random.uniform(12.9129359, 12.9529359)
        long = random.uniform(80.2105887, 80.2505887)
        model = Order.from_dict({'id': str(uuid.uuid4()),
                              'lat': lat,
                              'long': long})
        orders.append(model)

    return orders

from django.views.decorators.csrf import ensure_csrf_cookie


class RestApi(APIView):
    # @ensure_csrf_cookie
    def get(self, request):
        start_time = time.time()

        # store = OrderStore(TenderCuts())
        # orders = store.fetch()
        orders = make_orders()

        dist = DistributionCenter(0, 12.9329359, 80.2305887)

        eng = Engine(dist)
        routes = eng.generate_routes(orders)
        routes = [r.as_dict() for r in routes]
        end_time = time.time()
        count = 0
        for route in routes:
            count += len(route['orders'])


        print ("===============")
        print (len(routes))
        print (count)
        print (end_time - start_time)

        return Response({'route': routes})

