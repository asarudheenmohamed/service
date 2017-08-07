"""Test Otp send signup and forgot password."""
import pytest

from app.core.lib.otp_controller import *


@pytest.mark.django_db
class TestOtp:
    """Test otp for forgot and signup method."""

    def test_otp_forgot(self, rest):
        """Test otp for forgot method.

        Args:
         auth_rest(pytest fixture):user requests
         otp_type(FORGOT):user forgot method otp

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp

        """
        response = rest.get(
            "/user/otp_view/9908765678/?otp_type=FORGOT",
            format='json')
        assert response.data['mobile'] == "9908765678"
        otp = response.data['otp']
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=text&otp_type=FORGOT",
            format='json')
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=voice&otp_type=FORGOT",
            format='json')
        otp1 = response.data['otp']
        assert otp == otp1
        assert response.data['mobile'] == '9908765678'

    def test_otp_signup(self, rest):
        """Test otp for signup methodotp_type
        Args:
         auth_rest(pytest fixture):user requests
         otp_type(SIGNUP):user signup method otp

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp

        """
        response = rest.get(
            "/user/otp_view/9908765678/?otp_type=SIGNUP",
            format='json')
        assert response.data['mobile'] == "9908765678"
        otp = response.data['otp']
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=text&otp_type=SIGNUP",
            format='json')
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=voice&otp_type=SIGNUP",
            format='json')import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
from rest_framework.test import APIClient
import uuid
import redis
from rest_framework import viewsets, generics, mixins


@pytest.mark.django_db
class TestChangePassword:

    def test_change_password(self, auth_rest):
        response = auth_rest.post(
            "/user/change_password/",
            data={"new_password": "qwerty123"},
            format='json')
        # assert not isinstance(response, None)
        assert response.data['status'] is True

        otp1 = response.data['otp']
        assert otp == otp1
        assert response.data['mobile'] == '9908765678'

    def test_otp_verified_validation(self, rest):
        """Test otp veried validation.

        Args:
         rest(pytest fixture):user requests
         otp_type(LOGIN):user login method otp

        Asserts:
            Check response mobile is equal to test mobile number
            Check response status is equal to True
            Check response message is equal to 'succesfuly verified'

        """
        response = rest.get(
            "/user/otp_view/9908765678/?otp_type=LOGIN",
            format='json')
        assert response.data['mobile'] == "9908765678"
        otp_obj = Otpview()
        otp = otp_obj.get_object(9908765678, 'LOGIN')
        response = rest.get(
            "/user/otp_validation/9908765678/?type=LOGIN&otp={}".format(
                otp.otp),
            format='json')
        assert response.data['status'] == True
        assert response.data['message'] == 'succesfuly verified'

    def test_otp_invalid_validation(self, rest):
        """Test otp for invalid otp.

        Args:
         rest(pytest fixture):user requests
         otp_type(FORGOT):user LOGIN method otp validation

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp
            Check response message is equal to 'Invalid your OTP'

        """
        response = rest.get(
            "/user/otp_validation/9908765678/?otp_type=LOGIN&otp=1234",
            format='json')
        assert response.data['status'] == False
        assert response.data['message'] == 'Your OTP is Invalid'

    def test_otp_mode_login(self, rest, mock_user):
        """Test login OTP mode
        Args:
         rest(pytest fixture):user requests
         otp_mode(bol):user if otp via login otp mode is true otherwise False

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp
            Check response message is equal to 'Invalid your OTP'

        """
        response = rest.post(
            "/user/login/",
            {"email": mock_user.phone,
             "password": mock_user.password, "otp_mode": True})

        print(response.data)
        assert response.data['reward_points'] == 202
        assert response.data['email'] == mock_user.email
