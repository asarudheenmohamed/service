from app.driver.lib import ShadowFaxDriverController
from app.driver.models import *
import pytest

@pytest.fixture
def shadowfax():
    return ShadowFaxDriverController()

@pytest.mark.django_db(transaction=True)
@pytest.mark.incremental
class TestShadowFax:

    def test_shadowfax_fetch(self, shadowfax):
        assert shadowfax.driver.phone == str(9999999999)

    def test_place_order(self, shadowfax):
        responses = shadowfax.push_orders()

        # assert len(responses) == 0
        assert responses[0].status == "ACCEPTED"

    def test_callback_assigned(self, shadowfax):
        data = {
            "rider_name": "Dipesh",
            "sfx_order_id": 3427560,
            "allot_time": "2017-02-22T04:54:21.000000Z",
            "client_order_id": "986890898798",
            "order_status": "ALLOTTED",
            "rider_contact": "9986312121",
        }

        shadowfax.update_order(data)

        sfx_update = ShadowFaxUpdates.objects.filter(sfx_order_id=3427560)
        assert len(sfx_update) > 0
        assert sfx_update[0].sfx_order_id == str(3427560)

