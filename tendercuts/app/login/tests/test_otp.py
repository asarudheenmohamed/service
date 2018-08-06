"""Test all Otp methods."""
import pytest
import redis
from rest_framework.test import APIClient
from django.conf import settings
from app.core.lib import cache


@pytest.mark.django_db
class TestOtp:
    """Send Otp.

    Asserts:
     Check Response mobile number is equals to test mobile number

    """

    def test_otp(self, rest):
        """Test Otp send customer mobile number."""
        response = rest.get("/user/otp/9080804360/", format='json')
        assert not isinstance(response, type(None))

        assert response.data['mobile'] == "9080804360"


@pytest.mark.django_db
class TestResendOtp:
    """ Send OTP and Resend OTP.
        params:
          mobile(str): Phone number to send OTP
          resend (str): OTP send types are text ot voice

        1.check that response is not type(None)
        2.check that response mobile number is equal to sended mobile number

    """

    def test_otp(self, rest):
        """Send Otp in customer mobile Number.

        Params:
           rest(pytest fixture): api client
           mobile(int): customer mobile number

        Returns:
            rerurn in api client

        Asserts:
            check sent customer mobile number is equal to response mobile number

        """
        response = rest.get(
            "/user/forgot_password_otp/9080804360/",
            format='json')
        assert not isinstance(response, type(None))
        assert response.data['mobile'] == "9080804360"

    @pytest.mark.parametrize("resend_type", (
        ["text"],
        ["voice"],
    ))
    def test_resend_otp_methods(self, rest, resend_type):
        """Resend Otp in text method customer mobile Number.

        Params:
           rest(pytest fixture): api client
           mobile(int): customer mobile number
           resend_type(str): type of sent otp  in text method or voice method

        Returns:
            rerurn in api client

        Asserts:
            check sent customer mobile number is equal to response mobile number

        """
        response = rest.get(
            "/user/forgot_password_otp/9080804360/?resend_type={}".format(
                resend_type),
            format='json')
        assert not isinstance(response, type(None))
        assert response.data['mobile'] == "9080804360"


@pytest.mark.django_db
class TestOtpMethods:
    """Test Otp all methods."""

    def test_forgot_otp(self, rest):
        """Test Forgot method Password Otp.

        Asserts:
         Check response mobile number is equals to test mobile number.
         Check otp.

        """
        response = rest.get(
            "/user/forgot_password_otp/9080804360/", format='json')
        assert not isinstance(response, type(None))
        assert response.data['mobile'] == "9080804360"

        # redis_conn = redis.StrictRedis(**settings.REDIS)
        # otp = redis_conn.get("{}:{}".format("FORGOT_OTP", "9080804360"))
        otp = cache.get_key("{}:{}".format("FORGOT_OTP", "9080804360"))
        response = rest.get(
            "/user/forgot_password_otp/9080804360/", format='json')
        assert response.data['mobile'] == "9080804360"
        otp1 = cache.get_key("{}:{}".format("FORGOT_OTP", "9080804360"))
        assert otp == otp1

    def test_raise_error(self, rest):
        """Send otp from Test unknown customer mobile number.

        Raises:
            customer Not found.
        """
        response = rest.get(
            "/user/forgot_password_otp/9080804360111/", format='json')

        assert response.data['detail'] == "User does not exists"


@pytest.mark.django_db
class TestUserFetch:
    """Test user fetching data."""

    def test_user_fetch(self, auth_rest):
        """Test Fetch from user data."""
        response = auth_rest.get(
            "/user/fetch/?phone=9080804360", format='json')
        assert not isinstance(response, type(None))
        assert response.status_code == 200
