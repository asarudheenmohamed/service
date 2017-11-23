"""End point to verify the Otp."""
import logging
from rest_framework.response import Response
from rest_framework import viewsets
from app.otp.lib.otp_controller import OtpController

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpVerifyApi(viewsets.ModelViewSet):
    """Verify the Otp."""

    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """Check whether the customer entered otp is correct or not.

        params:
            mobile (str): New user mobile number
            otp_mode(int): otp types such as LOGIN,SIGNUP and FORGOT
            otp(int): customer entered otp

        Returns:
            Otp verified status

        """
        type_ = self.request.data['otp_mode']
        customer_otp = self.request.data['otp']
        phone = self.request.data['mobile']

        otp_obj = OtpController(logger)
        # get otp object
        logger.info('To get a otp for this number:{}'.format(phone))
        otp = otp_obj.get_otp(phone, type_)
        # verify the otp
        logger.info("to verifying the otp")
        is_verified = otp_obj.otp_verify(otp, customer_otp)

        logger.info("otp verified")

        if is_verified == True:
            message = 'Successfully verified'
        else:
            message = 'Your OTP is Invalid'

        return Response(
            {'status': is_verified,
             'message': message})
