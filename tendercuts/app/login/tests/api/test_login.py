import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
import uuid

class TestApiLogin:
    def test_endpoint_exists(self, rest):
        response = rest.get("/user/login/", format='json')
        assert type(response) is not HttpResponseNotFound


    def test_driver_login(self, rest, mock_user):
        """
        """
        response = rest.post(
                "/user/login/",
                {"username": mock_user.username,
                 "password": mock_user.password},
                format='json')

        assert response.data['status'] is True


    def test_signup_login(self, rest, mock_user):
        phno = randint(8000000000, 9999999999)
        password = "foobarbaz"
        email = "{}@test.com".format(uuid.uuid4())
        response = rest.post(
                "/user/signup/",
                {"email": email,
                 "password": password,
                 "name": mock_user.fullname,
                 "phone": str(phno)},
                format='json')

        assert response.data['status'] is True
