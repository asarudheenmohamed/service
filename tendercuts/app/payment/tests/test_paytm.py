from app.payment.lib import controller
from app.payment.lib import gateway
import time
import pytest


@pytest.fixture
def gw():
    return gateway.PaytmGateway()


@pytest.mark.django_db
@pytest.mark.incremental
class TestPaytmGateway:
    """Payu GW tests."""

    def _test_payment_status(self, gw):
        """Assert if the api is hit correctly."""
        # works only in PROD
        order_id = "800025242"
        payu_status = gw.check_payment_status(order_id)

        assert payu_status is True
