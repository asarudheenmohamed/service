"""Integration tests for card payment using APIs."""

from pytest_bdd import parsers
import pytest
import juspay
from splinter import Browser

from pytest_bdd import given, when, then, scenario
from app.payment.serializer import PaymentModeSerializer
from app.payment.models import PaymentMode
from app.core.models import SalesFlatOrder
from app.core.lib.test.utils import GenerateOrder


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
#     "User starts a transaction via paytm"
# )
# def test_new_paytm_payment_success(cache):
#     pass


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
@given('Customer starts the transaction via card')
def customer_transaction_via_card(
        auth_rest,
        juspay_dummy_card1,
        user_order,
        cache):
    """Start the transaction."""
    user_order.status = "pending_payment"
    user_order.save()

    juspay_dummy_card1.order_id = user_order.increment_id
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

@given('Customer starts the transaction via paytm')
def customer_transaction_via_paytm(
        auth_rest,
        user_order,
        cache):
    """Start the transaction."""
    user_order.status = "pending_payment"
    user_order.save()

    paytm_wallet = PaymentMode(
        title="Paytm",
        method="juspay",
        gateway_code="WALLET",
        gateway_code_level_1="PAYTM",
        priority=1,
        order_id=user_order.increment_id
    )

    serialized_data = PaymentModeSerializer(paytm_wallet)
    # convent model to py dict and remove the gateway_code so we get None in
    # dict
    data = serialized_data.data

    # start transaction
    response = auth_rest.post("/payment/modes/", data=data)
    assert response.status_code == 200

    return response

@given('User places an order')
def user_order(mock_user):
    order = GenerateOrder().generate_order(mock_user.entity_id)
    return order


####
#  Whens
####

@when('Customer pays succesfully with card')
def customer_pays_sucessfully_with_card(customer_transaction_via_card):
    with Browser('chrome') as browser:
        browser.visit(customer_transaction_via_card.json()['url'])
        css_sel = 'button.success'
        browser.is_element_not_present_by_css(css_sel, wait_time=7)
        browser.find_by_css('button.success')[0].click()

# @when('Customer pays succesfully with paytm')
# def customer_pays_sucessfully_with_paytm(customer_transaction_via_paytm):
#     with Browser('chrome') as browser:
#         import pdb
#         pdb.set_trace()
#         browser.visit(customer_transaction_via_paytm.json()['url'])
#         browser.is_element_present_by_css('form#loginForm', wait_time=20)
#         browser.fill(name='username', value='7777777777')
#         browser.fill(name='username', value='Paytm12345')
#         browser.find_by_css('button.btn-primary')[0].click()
#
#         browser.is_element_present_by_name('creditcard-form', wait_time=10)
#         browser.find_by_css('div.btn-submit')[0].click()
#         css_sel = 'button.success'
#         # browser.find_by_css('button.success')[0].click()


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
def verify_transaction(user_order):
    """Assert Transaction.

    1. Check if the user is created in juspay
    2. Order status
    3. Transaction URL is generated

    """
    juspay_order = juspay.Orders.status(order_id=user_order.increment_id)
    assert juspay_order.status == 'CHARGED'

    # order = SalesFlatOrder.objects.filter(
    #     increment_id=generate_mock_order.increment_id).first()
    # assert order.status == "pending"
    # TODO add receiving callback step here. due to localhost restrictions not done


@then("Card is saved")
def verify_saved_card(auth_rest):
    """Asserts:
        Card is saved in juspay.
    """
    response = auth_rest.get("/payment/modes/")
    assert response.status_code == 200

    # in the second scenario, the user already has a card saved. so chec
    # the card.
    card = filter(
        lambda payment: payment['gateway_code'] == 'CARD',
        response.json()['results'])[0]
    assert len(str(card['gateway_code_level_1'])) > 10


