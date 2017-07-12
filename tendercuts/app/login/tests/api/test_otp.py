"""Test Otp send signup and forgot password."""
import pytest


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
