from app.sale_order.models import ScheduledDelivery, ExpressDelivery
from django.http import HttpResponseNotFound
import datetime
import pytest


@pytest.mark.django_db
class TestDeliveryModel:
    """
    Tests for model delivery
    """

    def test_delivery_fetch(self):
        """
        Check delivery
        """
        assert ScheduledDelivery() is not None

    def test_delivery_cost(self):
        """
        Verify delivery cost
        """
        assert ExpressDelivery().cost == 49

    def test_slots_available(self):
        """
        Verify slots availabilty
        """
        assert ScheduledDelivery().is_slots_available() is True
        assert ExpressDelivery().is_slots_available() is True

        assert ExpressDelivery().is_slots_available(
            now=datetime.time(20, 0, 1)) is False
        assert ExpressDelivery().is_slots_available(
            now=datetime.time(6, 29, 59)) is False

    def test_slots(self):
        """
        Asserts:
            1. At 12 only 3 slots are there
            2. At 5 only 4 slots are there
            3. At 19 only 2 are there

        """
        delivery = ScheduledDelivery()
        now = datetime.datetime.now(tz=delivery.tz)
        dt_now = now.replace(hour=9, minute=0)
        slots = delivery.available_slots(now=dt_now)

        today = [s for s in slots if s['date']
                 == str(datetime.date.today())][0]
        assert len(slots) == 2
        assert len(today['times']) == 3

        dt_now = now.replace(hour=12)

        slots = delivery.available_slots(now=dt_now)

        today = [s for s in slots if s['date']
                 == str(datetime.date.today())][0]
        assert len(slots) == 2
        assert len(today['times']) == 2

        dt_now = now.replace(hour=5)
        slots = delivery.available_slots(now=dt_now)
        today = [s for s in slots if s['date']
                 == str(datetime.date.today())][0]
        assert len(slots) == 2
        assert len(today['times']) == 4
        # ["9:00 - 11:00", "11:00 - 13:00", "17:00 - 19:00", "19:00 - 21:00"]

        dt_now = now.replace(hour=19)
        slots = delivery.available_slots(now=dt_now)
        assert len(slots) == 1


@pytest.mark.django_db
class TestDeliveryRestApi:

    def test_endpoint_exists(self, auth_rest):
        response = auth_rest.get("/sale_order/delivery_slots/", format='json')
        assert not isinstance(response, HttpResponseNotFound)

    def test_endpoint(self, auth_rest):
        response = auth_rest.get("/sale_order/delivery_slots/", format='json')
        print(response.data)
        assert len(response.data) == 2
        assert response.data[0]['name'] == "Scheduled Delivery"
        assert response.data[1]['name'] == "Express Delivery"
