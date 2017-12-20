"""Integration tests for card payment using APIs."""

from pytest_bdd import parsers
import pytest
import juspay
from splinter import Browser

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


# @pytest.mark.django_db
# @scenario(
#     'card.feature',
#     'User starts a transaction via a saved card'
# )
# def test_saved_card_payment_success(cache):
#     pass


####
#  Givens
####
@given('Customer starts the transaction')
def customer_transaction(
        auth_rest,
        juspay_dummy_card1,
        generate_mock_order,
        cache):
    """Start the transaction."""
    generate_mock_order.status = "pending_payment"
    generate_mock_order.save()

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

    return response


# Reuse the mock order fixture
given(
    'User places an order',
    fixture='generate_mock_order')


####
#  Whens
####

@when('Customer pays succesfully')
def customer_pays_sucessfully(customer_transaction):
    with Browser('chrome') as browser:
        browser.visit(customer_transaction.json()['url'])
        css_sel = 'input.success'
        browser.is_element_not_present_by_css(css_sel, wait_time=4)
        browser.find_by_css('input.success')[0].click()


# @when("the customer successfully starts payment via a saved card")
# def juspay_savedcard_transaction(auth_rest, generate_mock_order, cache):
#     """Start the transaction."""
#     card = cache['saved_card']
#     card['order_id'] = generate_mock_order.increment_id
#
#     # start transaction
#     response = auth_rest.post("/payment/modes/", data=card)
#     assert response.status_code == 200
#
#     cache['response'] = response.json()


####
#  Thens
####
@then("Transaction is successfull")
def verify_transaction(generate_mock_order):
    """Assert Transaction.

    1. Check if the user is created in juspay
    2. Order status
    3. Transaction URL is generated

    """
    juspay_order = juspay.Orders.status(order_id=generate_mock_order.increment_id)
    assert juspay_order.status == 'CHARGED'

    order = SalesFlatOrder.objects.filter(
        increment_id=generate_mock_order.increment_id).first()
    assert order.status == "pending"


@then("Card is saved")
def verify_saved_card(auth_rest, generate_mock_order):
    """Asserts:
        Card is saved in juspay.
    """
    response = auth_rest.get("/payment/modes/")
    assert response.status_code == 200

    # in the second scenario, the user already has a card saved. so chec
    # the card.
    card = response.data['results'][0]
    assert len(str(card['gateway_code_level_1'])) > 10


