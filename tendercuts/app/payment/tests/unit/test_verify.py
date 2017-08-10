"""Payment Status API for all PG."""

from app.payment.lib import controller
from app.payment.lib import gateway
import pytest


@pytest.mark.django_db
class TestPaymentVerify:
    """Payu GW tests."""

    @pytest.mark.parametrize("gw,order_id,expected_status", (
        [gateway.PaytmGateway, "800025242", False],
        [gateway.Payu, "500008792", True],
    ))
    def test_payment_status(self, gw, order_id, expected_status):
        """Assert if the api is hit correctly."""
        status = gw().check_payment_status(order_id)
        assert status is expected_status
