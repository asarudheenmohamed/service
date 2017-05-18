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
