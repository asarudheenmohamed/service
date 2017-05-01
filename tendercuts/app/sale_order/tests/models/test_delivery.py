from app.sale_order.models import *
from django.http import HttpResponseNotFound
import datetime

class TestDeliveryModel:
    def test_delivery_fetch(self):
        assert ScheduledDelivery() is not None

    def test_delivery_cost(self):
        assert ScheduledDelivery().cost == 0
        assert ExpressDelivery().cost == 49

    def test_slots_available(self):
        assert ScheduledDelivery().is_slots_available() is True
        assert ExpressDelivery().is_slots_available() is True

        assert ExpressDelivery().is_slots_available(
                now=datetime.time(20, 0, 1)) is False
        assert ExpressDelivery().is_slots_available(
                now=datetime.time(6, 29, 59)) is False

    def test_slots(self):
        delivery = ScheduledDelivery()
        now = datetime.datetime.now(tz=delivery.tz)

        dt_now = now.replace(hour=12)
        slots = delivery.available_slots(now=dt_now)
        assert len(slots) == 3
        print (slots)
        assert len(slots[0]['times']) == 2

        dt_now = now.replace(hour=5)
        slots = delivery.available_slots(now=dt_now)
        print(slots)
        assert len(slots) == 3
        assert len(slots[0]['times']) == 4
            # ["9:00 - 11:00", "11:00 - 13:00", "17:00 - 19:00", "19:00 - 21:00"]

        dt_now = now.replace(hour=19)
        slots = delivery.available_slots(now=dt_now)
        print(slots)
        assert len(slots) == 2

class TestDeliveryRestApi:

    def test_endpoint_exists(self, auth_rest):
        response = auth_rest.get("/sale_order/delivery_slots/", format='json')
        assert type(response) is not HttpResponseNotFound

    def test_endpoint(self, auth_rest):
        response = auth_rest.get("/sale_order/delivery_slots/", format='json')
        print(response.data)
        assert len(response.data) == 2
        assert response.data[0]['name'] == "Scheduled Delivery"
        assert response.data[1]['name'] == "Express Delivery"

