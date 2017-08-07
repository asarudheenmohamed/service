"""Test new referred user reward amount transaction."""
import json
import uuid
from random import randint
import os

import pytest
import requests
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from app.core.lib.magento import Connector
from app.core.lib.order_controller import OrderController
from app.core.lib.test.utils import *
from app.core.models.customer.core import *
from app.core.lib.user_controller import *

from django.conf import settings


@pytest.fixture(scope='session')
def user():
    """Generate new user signup details."""
    return {'phno': randint(8000000000, 9999999999),
            'password': "rewardpoint123",
            'email': "{}@test.com".format(uuid.uuid4())}


@pytest.fixture(scope='session')
def test_user_reward(test_user):
    """Return User reward amount.

    Params:
        test_user(pytest fixture): return in test user id

    """
    user_reward_obj = CustomerController.load_customer_obj(test_user)

    return user_reward_obj.__dict__['_flat']['reward_points']


@pytest.fixture(scope='session')
def new_user_details(user):
    """Return User reward amount.

    Params:
        test_user(pytest fixture): return in test user id

    """
    user_reward_obj = CustomerSearchController.load_by_phone_mail(user['phno'])

    return user_reward_obj


@pytest.mark.django_db
class TestSignUp:
    """Test New user create and reward amount added refered user."""

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
        baseurl = settings.MAGENTO['url'] + settings.MAGENTO['servicepoint']
        url = os.path.join("http://" + baseurl + "index/createCustomer")
        response = requests.post(
            url, data=json.dumps(data))
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

    def test_check_new_user_reward_point(self, auth_rest, user):
        """Check reward point amount for new user.

        Params:
           rest(pytest fixture): api client
           user(pytest fixture): return sign up user details

        Asserts
            1.check reward amount added in new user

        """
        fetch_obj = auth_rest.get(
            "/user/fetch/?phone={}&email={}" .format(
                user['phno'], user['email']))
        assert fetch_obj.json()['attribute'][0]['value'] == 50

    def test_new_user_order_place(self, new_user_details):
        """Order placed in new user.

        Params:
           new_user_details(pytest fixture): basic information of new user

        Asserts
            2.Check order placed customer id is equal to new user id

        """
        order_obj = GenerateOrder()
        order_obj = order_obj.generate_order(
            new_user_details.customer.entity_id)
        conn = Connector()
        controller = OrderController(conn, order_obj)
        controller.complete()

        assert order_obj.customer_id == new_user_details.customer.entity_id

    def test_check_reward_amount(self, auth_rest, test_user_reward, test_user):
        """Check Reward Point amount in test user.

        Params:
           rest(pytest fixture): api client
           test_user(pytest fixture): return in test user id
           test_user_reward: test user reward amount

        Asserts:
           checks whether 50 rs credited to referral user on completing
           the first order of refered user

        """
        user_basic_info = CustomerSearchController.load_basic_info(test_user)

        fetch_obj = auth_rest.get("/user/fetch/?phone={}&email={}" .format(
            user_basic_info[2], user_basic_info[1]))

        assert fetch_obj.json()['attribute'][0][
            'value'] == test_user_reward + 50
