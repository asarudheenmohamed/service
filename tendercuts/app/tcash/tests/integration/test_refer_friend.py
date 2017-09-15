"""Refer a friend scenario testing."""

import pytest
from pytest_bdd import given, when, then, scenario
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.test import generate_customer, auth_client, GenerateOrder
from app.core.lib.order_controller import OrderController


@pytest.mark.django_db
@scenario(
    'refer_friend.feature',
    'Refer a friend',
)
def test_refer_friend():
    pass


"""Cache containes.
1. new_customer
2. authenticated rest.
"""


@given('A new user signs up via referal link')
def new_signup(cache):
    """Create a new customer."""
    customer_data = generate_customer()
    customer = CustomerSearchController.load_by_id(customer_data['entity_id'])

    cache["new_customer"] = customer
    cache["authenticated_rest"] = auth_client(customer)


@given("logs into his account")
def login(cache, rest):
    new_customer = cache["new_customer"]

    data = {"email": new_customer.email, "password": '12345678'}
    response = rest.post("/user/login", data=data)

    assert response.status_code == 200, "User was unable to login"
    assert response.json()['reward_points'] == 0


@given("is referred by an existing user")
def refer_customer(cache, mock_user):
    authenticated_rest = cache["authenticated_rest"]

    referral_response = authenticated_rest.post(
        "/tcash/referral",
        {'user_id': mock_user.entity_id})

    assert referral_response.status_code == 200, "Unable to reach endpoint"
    resp = referral_response.json()

    assert resp['status'] == True, "Endpoint returned false"
    assert "50" in resp['message'], "Invalid message sent"


@given("the new user get 50 in his account")
def get_fifty(cache):
    authenticated_rest = cache["authenticated_rest"]
    new_customer = cache["new_customer"]
    fetch_obj = authenticated_rest.get(
        "/user/fetch/?phone={}".format(new_customer.mobilenumber))

    resp = fetch_obj.json()
    assert resp['attribute'][0][
        'value'] == 50, "Signed up user did not receive 50 points"


@when("the new user places an order")
def place_order(cache, magento):
    new_customer = cache["new_customer"]
    order_obj = GenerateOrder()
    order_obj = order_obj.generate_order(new_customer.entity_id)

    controller = OrderController(magento, order_obj)
    controller.complete()


@then("the referee get 50 in his account")
def check_bonus(auth_rest, mock_user):
    """Doc here"""
    fetch_obj = auth_rest.get(
        "/user/fetch/?phone={}".format(mock_user.mobilenumber))

    resp = fetch_obj.json()
    assert resp['attribute'][0][
        'value'] == 50, "Referee did not receive 50 points"
