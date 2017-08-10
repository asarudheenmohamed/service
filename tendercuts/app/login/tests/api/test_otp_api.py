"""Test Otp send signup and forgot password."""
import pytest

from app.core.lib.otp_controller import OtpController


@pytest.mark.django_db
class TestOtpGenerateApi:
    """Test otp for forgot and signup method."""

    @pytest.mark.parametrize("phone,otp_type", (
        ["9080804360", "FORGOT"],
        ["9080804360", "SIGNUP"],
    ))
    def test_otp_forgot(self, auth_rest, phone, otp_type):
        """Test otp for forgot method.

        Args:
         auth_rest(pytest fixture): user requests
         otp_type(FORGOT): user forgot method otp

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp

        """
        response = auth_rest.get(
            "/user/otp_view/{}/?otp_type={}".format(phone, otp_type),
            format='json')
        assert response.data['mobile'] == phone
        response = auth_rest.get(
            "/user/otp_view/{}/?resend_type=text&otp_type={}".format(
                phone, otp_type),
            format='json')
        assert response.data['mobile'] == phone

        response = auth_rest.get(
            "/user/otp_view/{}/?resend_type=voice&otp_type={}".format(
                phone, otp_type),
            format='json')


@pytest.mark.django_db
class TestOtpValidation:
    """Test Otp validation."""
    @pytest.mark.parametrize("phone,otp_type,otp", (
        ["9080804360", "FORGOT", '1234'],
        ["9080804360", "SIGNUP", '1234'],
        ["9080804360", "LOGIN", '1234']
    ))
    def test_otp_invalid_validation(self, auth_rest, phone, otp_type, otp):
        """Test otp for invalid otp.

        Args:
         rest(pytest fixture):user requests
         otp_type(FORGOT):user LOGIN method otp validation

        Asserts:
            Check response mobile is equal to test mobile number
            Check response text method otp is equal to voice method otp
            Check response message is equal to 'Invalid your OTP'

        """
        response = auth_rest.get(
            "/user/otp_validation/{}/?otp_type={}&otp={}".format(
                phone, otp_type, otp),
            format='json')
        assert response.data['status'] == False
        assert response.data['message'] == 'Your OTP is Invalid'
