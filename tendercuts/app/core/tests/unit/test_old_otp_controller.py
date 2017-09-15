"""End Point for the test redis controller."""
import pytest

from app.otp.lib.otp_controller import OtpController
from rest_framework import exceptions


@pytest.mark.django_db
class TestOtpController:
    """Test OTP controller."""

    def test_otp_create_sucess(self, mock_user):
        """Test OTP controller getOtp. (sligtly a integration test)

        Asserts:
            1. If OTP is generated/fetched.
            2. If the OTP is verified (success).

        """
        ctrl = OtpController()
        otp = ctrl.get_otp(
            mock_user.mobilenumber,
            OtpController.LOGIN)

        assert otp.mobile == mock_user.mobilenumber
        assert otp.otp is not None

        assert ctrl.otp_verify(otp, otp.otp) is True

    def test_otp_create_failure(self, mock_user):
        """Test OTP controller getOtp. (sligtly a integration test)

        Asserts:
            1. If OTP is generated/fetched.
            2. If the OTP is verified (failed)

        """
        ctrl = OtpController()
        otp = ctrl.get_otp(
            mock_user.mobilenumber,
            OtpController.LOGIN)

        assert otp.mobile == mock_user.mobilenumber
        assert otp.otp is not None

        assert ctrl.otp_verify(otp, "111111111") is False

    def test_otp_create_invalid_customer(self, mock_user):
        """Test OTP controller getOtp.

        Asserts:
          if CustomerNotFound exception is raise

        """
        with pytest.raises(exceptions.PermissionDenied):
            otp = OtpController().get_otp(
                "FAKENUMBER",
                OtpController.LOGIN)
