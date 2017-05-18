from app.driver.lib import ShadowFaxDriverController
from app.driver.models import *
import pytest
import time
import requests


@pytest.fixture
def shadowfax():
    return ShadowFaxDriverController()


@pytest.mark.django_db(transaction=True)
@pytest.mark.incremental
class _TestShadowFax:

    def test_mock_order_create(self, generate_mock_order):
        # move the order to out_delivery and assign a driver

        sales_order = generate_mock_order
        sales_order.driver_id = 8
        sales_order.status = "out_delivery"
        # sales_order.status = "processing"
        sales_order.save()
        time.sleep(1)

    def test_shadowfax_fetch(self, shadowfax):
        assert shadowfax.driver.phone == str(9999999999)

    def test_place_order(self, shadowfax, generate_mock_order):
        responses = shadowfax.push_orders()

        # assert len(responses) == 0
        assert responses[0].status == "ACCEPTED"
        sfx_update_accept = ShadowFaxUpdates.objects.filter(
            client_order_id=generate_mock_order.increment_id)
        assert len(sfx_update_accept) > 0
        assert sfx_update_accept[0].order_status == "ACCEPTED"

    def test_callback_assigned(self, shadowfax, generate_mock_order):
        data = {
            "rider_name": "Dipesh",
            "sfx_order_id": 3427560,
            "allot_time": "2017-02-22T04:54:21.000000Z",
            "client_order_id": generate_mock_order.increment_id,
            "order_status": "ALLOTTED",
            "rider_contact": "9986312121",
        }

        shadowfax.update_order(data)

        sfx_update_allotted = ShadowFaxUpdates.objects.filter(
            sfx_order_id=3427560)
        assert len(sfx_update_allotted) > 0
        assert sfx_update_allotted[0].sfx_order_id == str(3427560)

    def test_callback_assigned(self, shadowfax, generate_mock_order):
        data = {
            "rider_name": "Dipesh",
            "sfx_order_id": 3427560,
            "allot_time": "2017-02-22T04:54:21.000000Z",
            "client_order_id": generate_mock_order.increment_id,
            "order_status": "DELIVERED",
            "rider_contact": "9986312121",
        }

        # shadowfax.update_order(data)
        url = 'http://localhost:8000/drivers/sfx_update'
        post = requests.post(url, data=data)
        time.sleep(2)

        sfx_update_allotted = ShadowFaxUpdates.objects.filter(
            sfx_order_id=3427560)
        assert len(sfx_update_allotted) > 0
        assert sfx_update_allotted[0].order_status == "DELIVERED"
        sales_order = SalesFlatOrder.objects.filter(
            increment_id=generate_mock_order.increment_id)
        assert sales_order[0]
        assert sales_order[0].status == "complete"
