"""End point to resend the otp through text or voice method."""
import logging

from rest_framework import viewsets
from rest_framework.response import Response

from app.otp.lib.otp_controller import OtpController
from app.core.lib.communication import SMS

from app.core import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpRetryApi(viewsets.ModelViewSet):
    """Resend the Otp for Signup,login and forgot."""

    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """OTP resend to the user mobile Number.

        params:
            mobile (str): New user mobile number
            otp_mode(str): otp types are forgot otp or signup otp
            retry_mode(str): retry mode for text or voice methods

        Returns:
            status

        """
        phone = self.request.data['mobile']
        otp_mode = self.request.data['otp_mode']
        retry_mode = self.request.data['retry_mode']

        # retry the otp
        SMS().retry_otp(phone, retry_mode)

        logger.info('Otp sent retry {} method.'.format(retry_mode))

        return Response({'status': True, 'message': 'Successfully resend otp'})
