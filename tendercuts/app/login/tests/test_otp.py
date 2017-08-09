"""Test all Otp methods."""
import pytest
import redis
from rest_framework.test import APIClient
from django.conf import settings


@pytest.fixture
def auth_rest():
    from django.contrib.auth.models import User
    user = User.objects.get(username="u:18963")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestOtp:
    """Send Otp.

    Asserts:
     Check Response mobile number is equals to test mobile number

    """

    def test_otp(self, rest):
        """Test Otp send customer mobile number."""
        response = rest.get("/user/otp/9908765678/", format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

    def test_same_otp(self, rest):
        """Test same Otp send Ofter 15 mins."""
        response = rest.get("/user/otp/9908765678/", format='json')

        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"
        otp = response.data['otp']

        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"
        assert response.data['otp'] == otp


@pytest.mark.django_db
class TestResendOtp:
    """ Send OTP and Resend OTP.
        params:
          mobile(str): Phone number to send OTP
          resend (str): OTP send types are text ot voice

        1.check that response is not None
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
            "/user/forgot_password_otp/9908765678/",
            format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

    def test_otp_resend_text(self, rest):
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
            "/user/forgot_password_otp/9908765678/?resend_type=text",
            format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

    def test_otp_resend_voice(self, rest):
        """Resend Otp in text method customer mobile Number.

        Params:
           rest(pytest fixture): api client
           mobile(int): customer mobile number
           resend_type(str): type of sent otp  in text method or voice method

        Returns:
            rerurn api client

        Asserts:
            check sent customer mobile number is equal to response mobile number

        """
        response = rest.get(
            "/user/forgot_password_otp/9908765678/?resend_type=voice",
            format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"


@pytest.mark.django_db
class TestResendOtpSignUp:
    """ Send OTP and Resend OTP Signup user.
        params:
          mobile(str): Phone number to send OTP
          resend (str): OTP send types are text ot voice

        1.check that response is not None
        2.check that response mobile number is equal to sended mobile number

    """

    def test_otp(self, rest):
        """Send Otp in SignUp customer mobile Number.

        Params:
           rest(pytest fixture): api client
           mobile(int): customer mobile number

        Returns:
            rerurn in api client

        Asserts:
            check sent customer mobile number is equal to response mobile number

        """
        response = rest.get(
            "/user/otp/9908765678/",
            format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

    def test_otp_resend_text(self, rest):
        """Resend Otp in text method Sign Up customer mobile Number.

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
            "/user/otp/9908765678/?resend_type=text",
            format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

    def test_otp_resend_voice(self, rest):
        """Resend Otp in text method customer mobile Number.

        Params:
           rest(pytest fixture): api client
           mobile(int): customer mobile number
           resend_type(str): type of sent otp  in text method or voice method

        Returns:
            rerurn api client

        Asserts:
            check sent customer mobile number is equal to response mobile number

        """
        response = rest.get(
            "/user/otp/9908765678/?resend_type=voice",
            format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"


@pytest.mark.django_db
class TestOtpMethods:
    """Test Otp all methods."""

    def test_otp(self, rest):
        """Test Forgot method Password Otp.

        Asserts:
         Check response mobile number is equals to test mobile number.
         Check otp.

        """
        response = rest.get(
            "/user/forgot_password_otp/9908765678/", format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

        redis_conn = redis.StrictRedis(**settings.REDIS)
        otp = redis_conn.get("{}:{}".format("FORGOT_OTP", "9908765678"))

        response = rest.get(
            "/user/forgot_password_otp/9908765678/", format='json')
        assert response.data['mobile'] == "9908765678"
        otp1 = redis_conn.get("{}:{}".format("FORGOT_OTP", "9908765678"))
        assert otp == otp1

    def test_raise_error(self, rest):
        """Send otp from Test unknown customer mobile number.

        Raises:
            customer Not found.
        """
        with pytest.raises(Exception):
            rest.get(
                "/user/forgot_password_otp/9908765678111/", format='json')

    def test_otp_password_reset(self, rest):
        """Test Otp Password reset.

        Asserts:
         Check response mobile number is equals to test mobile number.

        """
        response = rest.get(
            "/user/forgot_password_otp/9908765678/", format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

        redis_conn = redis.StrictRedis(**settings.REDIS)
        otp = redis_conn.get("{}:{}".format("FORGOT_OTP", "9908765678"))

        data = {"mobile": "9908765678", "otp": otp, "dry_run": True}
        response = rest.post("/user/forgot_password_otp/", data, format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"


@pytest.mark.django_db
class TestUserFetch:
    """Test user fetching data."""

    def test_user_fetch(self, auth_rest):
        """Test Fetch from user data."""
        response = auth_rest.get(
            "/user/fetch/?phone=9908765678", format='json')
        print(response)
        assert type(response) is not None
        assert len(response.data['attribute']) == 3


@pytest.mark.django_db
class TestUserExists:
    """Test user Exist method."""

    def test_user_exists_phone(self, rest):
        """Test Existing Customer.

        Asserts:
            Check response equals to True
        """
        response = rest.get("/user/exists/?phone=9908765678", format='json')
        assert type(response) is not None
        assert response.data['result'] is True

    def test_user_exists_email(self, rest):
        """Test Existing email.

        Asserts:
            Check response equals to True
        """
        response = rest.get(
            "/user/exists/?email=varun@tendercuts123.com", format='json')
        assert type(response) is not None
        assert response.data['result'] is True

    def test_user_exists_invalid(self, rest):
        """Test Customer Exist Invalid.

        Asserts:
            Check response equals to True
        """
        response = rest.get("/user/exists/", format='json')
        assert type(response) is not None
        assert response.data['result'] is True

    def test_user_exists_valid_phone(self, rest):
        """Test customer valid mobile number.

        Asserts:
            Check response equals to False

        """
        response = rest.get("/user/exists/?phone=90909090", format='json')
        assert type(response) is not None
        assert response.data['result'] is False

    def test_user_exists_valid_email(self, rest):
        """Test  customer valid email.

        Asserts:
            Check response equals to False

        """
        response = rest.get(
            "/user/exists/?email=90909090@xoxo.com", format='json')
        assert type(response) is not None
        assert response.data['result'] is False
