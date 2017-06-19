"""Test new referred user reward amount transaction."""
import pytest
import requests
import json
import uuid
from random import randint
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.core.lib.test.test_utils_order_placed import *
from app.core.lib.order_controller import OrderController
from app.core.lib.magento import Connector
from app.core.models.customer.core import *


@pytest.fixture(scope='session')
def user():
    """Generate new user signup details."""
    return {'phno': randint(8000000000, 9999999999),
            'password': "rewardpoint123",
            'email': "{}@test.com".format(uuid.uuid4())}


@pytest.fixture(scope='session')
def test_user_reward(test_user):
    """Return User rewr amount.

    Params:
        test_user(pytest fixture): return in test user id

    """
    user_reward_obj = FlatCustomer.load_by_id(test_user)
    return user_reward_obj.__dict__['_flat']['reward_points']


@pytest.mark.django_db
class TestSignUp:
    """Test New user create and add referal reward amount."""

    def test_login_create_success(self, rest, user):
        """Create new User.

        Params:
           rest(pytest fixture): api client
           user(pytest fixture): return sign up user details

        1. Create  a new User
        2. Verify if the login happens with email and phonenumber

        Asserts:
            1. User created

        """
        data = {"firstname": "Test",
                "email": user['email'],
                "mobilenumber": user['phno'],
                "password": user['password']}
        response = requests.post(
            "http://localhost/tendercuts-site/index.php/servicelayer/index/createCustomer", data=json.dumps(data))
        assert response.json()['result'] == True

    def test_reward_amund_add_new_customer(self,
                                           rest,
                                           user,
                                           test_user,
                                           test_user_reward):
        """Reward Point amount add New customer and order placed.

        Params:
           rest(pytest fixture): api client
           user(pytest fixture): return sign up user details
           test_user(pytest fixture): return in test user id
           test_user_reward: test user reward amount

        Asserts
            1.Verify if the login happens with email and phnumber
            2.check reward amount added in new user
            2.Check order plased customer id is equal to new user id

        """
        data = {"email": user['email'], "password": user['password']}
        response = rest.post("/user/login", data=data)
        users = User.objects.get(
            username=("{}:{}".format('u', response.json()['entity_id'])))
        client = APIClient()
        client.force_authenticate(user=users)
        referral_response = client.post(
            "/tcash/referral", {'user_id': test_user})
        assert referral_response.status_code == 200
        assert referral_response.json()['status'] == True
        fetch_obj = rest.get(
            "/user/fetch/?phone={}&email={}" .format(
                user['phno'], user['email']))
        assert fetch_obj.json()['attribute'][0]['value'] == 50
        order_obj = GenerateOrder(
            response.json()['entity_id']).order
        assert response.json()['entity_id'] == order_obj.customer_id
        conn = Connector()
        controller = OrderController(conn, order_obj)
        response_data = controller.complete()

    def test_check_reward_amount(self, rest, test_user_reward, test_user):
        """Check Reward Point amount in test user.

        Params:
           rest(pytest fixture): api client
           test_user(pytest fixture): return in test user id
           test_user_reward: test user reward amount

        Asserts:
           checks whether 50 rs credited to referral user on completing
           the first order of refered user

        """
        user_basic_info = FlatCustomer.load_basic_info(test_user)
        fetch_obj = rest.get("/user/fetch/?phone={}&email={}" .format(
            user_basic_info[2], user_basic_info[1]))
        assert fetch_obj.json()['attribute'][0]['value'] == test_user_reward+50

