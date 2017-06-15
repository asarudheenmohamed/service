"""Test New Referred User reward amount Transection."""
import pytest
import requests
import json
import uuid
from random import randint
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.core.lib.test.test_utils_order_placed import *
    
@pytest.fixture(scope='session')
def user():
    """Generate new user signup details."""
    return {'phno' : randint(8000000000, 9999999999),
            'password':"poiut123",
            'email' : "{}@test.com".format(uuid.uuid4())
    }

@pytest.mark.django_db
class TestSignUp:
    """Test New user create and add referal reward amount."""
    
    def test_login_create_success(self,rest,user):
        """Create new User.
        
        Params:
           rest(pytest fixture): api client
           user(pytest fixture): return sign up user details

        1. Create  a new User
        2. Verify if the login happens with email and phnumber

        expected:
            1. User created
        
        """
        data={"firstname":"Test","email":user['email'],"mobilenumber":user['phno'],"password":user['password']}
        response = requests.post(
            "http://localhost/tendercuts-site/index.php/servicelayer/index/createCustomer",data=json.dumps(data))
        assert response.json()['result'] == True
    
    def test_reward_amund_add_new_customer(self,rest,user):
        """Reward Point amount add New customer and order plased.

        Params:
           rest(pytest fixture): api client
           user(pytest fixture): return sign up user details
        

        Asserts
            1.Verify if the login happens with email and phnumber
            2.check reward amount added in new user
            2.Check order plased customer id is equal to new user id
        
        """
        data={"email": user['email'],"password": user['password']}
        response = rest.post("/user/login",data=data)
        users = User.objects.get(
            username=("{}:{}".format('u', response.json()['entity_id'])))
        client = APIClient()
        client.force_authenticate(user=users)
        referral_response = client.post(
            "/tcash/referral",{'mobile':'9908765678'})
        assert referral_response.status_code == 200
        assert referral_response.json()['status'] == "Reward referral amount added "
        fetch_obj=rest.get(
            "/user/fetch/?phone={}&email={}" .format(user['phno'],user['email']))
        assert fetch_obj.json()['attribute'][0]['value'] == 50
        order_obj = GenerateOrder(
            response.json()['entity_id']).order
        assert response.json()['entity_id'] == order_obj.customer_id