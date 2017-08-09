"""This module is deprecated."""
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from app.core.lib.otp_controller import OtpController

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpValidation(APIView):
    """OTP Validation."""

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        """OTP validate in signup,forgot password and login method.

        params:
            mobile (str): New user mobile number
            type(int):otp types are forgot otp or signup otp

        Returns:
            Otp validation status

        """
        type_ = self.request.GET.get('otp_type')
        customer_otp = self.request.GET.get('otp')
        phone = kwargs['mobile']

        otp_obj = OtpController(logger)
        # get otp object
        otp = otp_obj.get_otp(phone, type_)
        # verify the otp
        is_verified = otp_obj.otp_verify(otp, customer_otp)

        if is_verified == True:
            message = 'succesfuly verified'
        else:
            message = 'Your OTP is Invalid'

        return Response(
            {'status': is_verified,
             'message': message})
