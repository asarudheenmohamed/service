import pytest
import juspay
import uuid


@pytest.fixture
def juspay_mock_order(generate_mock_order):
    """Fixture to create a mock order in JP gateway."""
    # create a dummy order
    order_id = generate_mock_order.increment_id

    # init the env
    from django.conf import settings
    juspay.api_key = settings.PAYMENT['JUSPAY']['id']
    juspay.environment = settings.PAYMENT['JUSPAY']['environment']

    # mock
    _ = juspay.Orders.create(
        order_id=order_id,
        amount=int(generate_mock_order.grand_total),
        return_url="http://staging.tendercuts.in:82/payment/juspay/")

    return generate_mock_order


@pytest.fixture
def juspay_dummy_card1():
    """
    Not saved in JP test
    """
    from app.payment.models import PaymentMode
    return PaymentMode(
        title="4242424242424242",
        pin="111",
        expiry_year="2020",
        expiry_month="10",
        method="juspay",
        gateway_code="CARD")


@pytest.fixture
def juspay_dummy_card2():
    """
    Saved in jp test
    """
    from app.payment.models import PaymentMode
    return PaymentMode(
        title="5105105105105100",
        pin="111",
        expiry_year="2020",
        expiry_month="10",
        method="juspay",
        gateway_code="CARD")
