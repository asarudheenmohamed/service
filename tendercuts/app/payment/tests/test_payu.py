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
class _TestPayuGateway:

    def test_mock_order(self, generate_mock_order):
        generate_mock_order.status = "pending_payment"
        generate_mock_order.save()
        # time.sleep(5)

    def test_filter_orders(self, payu_gw, generate_mock_order):
        orders = payu_gw.filter_orders([generate_mock_order], threshold=3)
        assert len(orders) == 1

    def test_payment_status(self, generate_mock_order, payu_gw):
        payu_status = payu_gw.check_payment_status([generate_mock_order])

        assert len(payu_status) == 1
        payu_status = payu_status[0]

        assert payu_status.amount_captured == "-1"
        assert str(payu_status.vendor_status) == 'Not Found'


@pytest.mark.django_db
@pytest.mark.incremental
class _TestPaymentAutomation:
    def test_mock_order(self, generate_mock_order):
        generate_mock_order.status = "pending_payment"
        generate_mock_order.save()

    def test_fetch_orders(self, payment, generate_mock_order):
        orders = payment.fetch_orders(
            threshold=3)
        assert len(orders) >= 1

    def test_payment_cancellation(self, generate_mock_order, payment):
        """
        TODO: Needs to be integrated
        """
        payment.fetch_pending_orders = lambda : [generate_mock_order]
        payu_status = payment.cancel_pending_orders()

        # assert len(payu_status) == 1
        # payu_status = payu_status[0]

        # assert payu_status.amount_captured == -1
        # assert payu_status.vendor_status is False




