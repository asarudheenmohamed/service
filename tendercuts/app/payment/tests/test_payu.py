from app.payment.lib import controller
from app.payment.lib import gateway
import time
import pytest


@pytest.fixture
def payu_gw():
    return gateway.Payu()


@pytest.fixture
def payment(payu_gw):
    return controller.PaymentAutomationController(
        payu_gw)


@pytest.mark.django_db
@pytest.mark.incremental
class TestPayuGateway:
    """Payu GW tests."""

    def test_payment_status(self, payu_gw):
        """Assert if the api is hit correctly."""
        order_id = "500008792"
        payu_status = payu_gw.check_payment_status(order_id)

        assert payu_status is True
