import pytest
import juspay
import uuid


@pytest.fixture
def juspay_mock_order_id():
    """
    Fixture to create a mock order in JP gateway
    """
    # create a dummy order
    order_id = str(uuid.uuid4())
    amount = 99

    # mock
    _ = juspay.Orders.create(
        order_id=order_id,
        amount=amount,
        return_url="http://staging.tendercuts.in:82/payment/juspay/")

    return order_id


@pytest.fixture
def juspay_mock_user():
    """
    Fixture to create a mock user.
    """
    return "juspay_18963"


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
        gateway_code="CARD",
        gateway_code_level_1=None)

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
        gateway_code="CARD",
        gateway_code_level_1=None)