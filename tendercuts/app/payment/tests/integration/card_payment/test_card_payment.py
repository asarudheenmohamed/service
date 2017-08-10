"""Integration tests for card payment using APIs."""

from pytest_bdd import parsers
import pytest
import juspay

from pytest_bdd import given, when, then, scenario
from app.payment.lib.gateway import JusPayGateway, JuspayTransaction
from app.payment.serializer import PaymentModeSerializer
from app.core.models import SalesFlatOrder


@pytest.mark.django_db
@scenario(
    'card.feature',
    "User starts a transaction via a new card"
)
def test_new_card_payment_success(cache):
    pass


@pytest.mark.django_db
@scenario(
    'card.feature',
    'User starts a transaction via a saved card'
)
def test_saved_card_payment_success(cache):
    pass


####
#  Givens
####
@given(parsers.cfparse(
    "Payment modes should atleast by {no_of_modes:Number}",
    extra_types=dict(Number=int)))
def list_modes(mock_user, auth_rest, no_of_modes, cache):
    """Fetch modes."""
    response = auth_rest.get("/payment/modes/")
    assert response.status_code == 200

    # bad test case.
    assert len(response.data['results']) >= no_of_modes

    # in the second scenario, the user already has a card saved. so chec
    # the card.
    if no_of_modes:
        card = response.data['results'][0]
        assert len(str(card['gateway_code_level_1'])) > 10
        cache['saved_card'] = card


# Reuse the mock order fixture
given(
    'places an order',
    fixture='generate_mock_order')


####
#  Whens
####
@when("the customer successfully starts payment via a new card")
def juspay_newcard_transaction(
        auth_rest,
        juspay_dummy_card1,
        generate_mock_order,
        cache):
    """Start the transaction."""
    juspay_dummy_card1.order_id = generate_mock_order.increment_id
    juspay_dummy_card1.priority = 100

    serialized_data = PaymentModeSerializer(juspay_dummy_card1)
    # convent model to py dict and remove the gateway_code so we get None in
    # dict
    data = serialized_data.data
    del data['gateway_code_level_1']

    # start transaction
    response = auth_rest.post("/payment/modes/", data=data)
    assert response.status_code == 200

    cache['response'] = response.json()


@when("the customer successfully starts payment via a saved card")
def juspay_savedcard_transaction(auth_rest, generate_mock_order, cache):
    """Start the transaction."""
    card = cache['saved_card']
    card['order_id'] = generate_mock_order.increment_id

    # start transaction
    response = auth_rest.post("/payment/modes/", data=card)
    assert response.status_code == 200

    cache['response'] = response.json()


####
#  Thens
####
@then("the transaction is initiated")
def verify_transaction(mock_user, generate_mock_order, cache):
    """Assert Transaction.

    1. Check if the user is created in juspay
    2. Order status
    3. Transaction URL is generated

    """
    response = cache['response']

    assert str(mock_user.entity_id) in str(response['customer_id'])
    assert juspay.Customers.get(id=response['customer_id'][0]) is not None

    assert juspay.Orders.status(
        order_id=generate_mock_order.increment_id) is not None
    assert juspay.Orders.status(
        order_id=generate_mock_order.increment_id).status == "PENDING_VBV"

    assert "https://sandbox.juspay.in/pay/" in response['url']
