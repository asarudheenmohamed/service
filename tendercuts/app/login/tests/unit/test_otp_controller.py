"""End point for the Test otp controller."""
import pytest

from app.core.lib.otp_controller import OtpController


@pytest.mark.parametrize("otp_type", [
    "FORGOT",
    "SIGNUP",
    "LOGIN",
])
@pytest.mark.django_db
def test_otpobj(otp_type):
    """Test Otp object.

    Args:
      otp_type(params):otp types

    Asserts:
      Check otp object mobile number is equal to test mobile number


    """
    otp_obj = OtpController()
    otp = otp_obj.get_otp(9908765678, otp_type)
    assert otp.mobile == 9908765678


@pytest.mark.django_db
def test_otp_create():
    """Test Otp creation.

    Args:
      otp_type(params):otp types

    Asserts:
      Check otp object mobile number is equal to test mobile number

    """
    otp_obj = OtpController()
    otp = otp_obj.create_otp(9908765678)
    assert otp.mobile == 9908765678


@pytest.mark.parametrize("otp_type", [
    "FORGOT",
    "SIGNUP",
    "LOGIN",
])
@pytest.mark.django_db
def test_otp_verify_false(otp_type):
    """Test Otp validation Talse condition.

    Args:
      otp_type(params):otp types

    Asserts:
      Check otp validation is equal to False


    """
    otp_obj = OtpController()
    otp = otp_obj.get_otp(9908765678, otp_type)
    otp_validation = otp_obj.otp_verify(otp, 4343)
    assert otp_validation == False


@pytest.mark.parametrize("otp_type", [
    "FORGOT",
    "SIGNUP",
    "LOGIN",
])
@pytest.mark.django_db
def test_otp_verify_true(otp_type):
    """Test Otp validation True condition.

    Args:
      otp_type(params):otp types

    Asserts:
      Check otp validation is equal to False

    """
    otp_obj = OtpController()
    otp = otp_obj.get_otp(9908765678, otp_type)
    otp_validation = otp_obj.otp_verify(otp, otp.otp)
    assert otp_validation == True
