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

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp

        """
        response = rest.get("/user/otp_view/9908765678/?type=1", format='json')
        assert response.data['mobile'] == "9908765678"
        otp = response.data['otp']
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=text&type=1",
            format='json')
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=voice&type=1",
            format='json')
        otp1 = response.data['otp']
        assert otp == otp1
        assert response.data['mobile'] == '9908765678'

    def test_otp_signup(self, rest):
        """Test otp for signup method.

        Args:
         auth_rest(pytest fixture):user requests

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp

        """
        response = rest.get("/user/otp_view/9908765678/?type=2", format='json')
        assert response.data['mobile'] == "9908765678"
        otp = response.data['otp']
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=text&type=2",
            format='json')
        response = rest.get(
            "/user/otp_view/9908765678/?resend_type=voice&type=2",
            format='json')
        otp1 = response.data['otp']
        assert otp == otp1
        assert response.data['mobile'] == '9908765678'

    def test_otp_verified_validation(self, rest):
        """Test otp veried validation.

        Args:
         rest(pytest fixture):user requests

        Asserts:
            Check response mobile is equal to test mobile number
            Check response status is equal to True
            Check response message is equal to 'succesfuly verified'


        """
        response = rest.get("/user/otp_view/9908765678/?type=1", format='json')
        assert response.data['mobile'] == "9908765678"
        otp_obj = Otpview()
        otp = otp_obj.get_object(9908765678, '1')
        response = rest.get(
            "/user/otp_validation/9908765678/?type=1&otp={}".format(otp.otp),
            format='json')
        assert response.data['status'] == True
        assert response.data['message'] == 'succesfuly verified'

    def test_otp_invalid_validation(self, rest):
        """Test otp for invalid otp.

        Args:
         rest(pytest fixture):user requests

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp
            Check response message is equal to 'Invalid your OTP'

        """
        response = rest.get(
            "/user/otp_validation/9908765678/?type=1&otp=1234",
            format='json')
        assert response.data['status'] == False
        assert response.data['message'] == 'Invalid your OTP'

    def test_otp_mode_login(self, rest, mock_user):
        """Test login OTP mode
        Args:
         rest(pytest fixture):user requests

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
        assert response.data['reward_points'] == 2100
        assert response.data['email'] == mock_user.email
