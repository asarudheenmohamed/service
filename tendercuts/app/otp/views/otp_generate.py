"""End point to provide the otp to the customer mobile number."""
import logging
from rest_framework import viewsets
from rest_framework.response import Response

from app.otp.lib.otp_controller import OtpController

from app.core import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpGenerateApi(viewsets.ModelViewSet):
    """Generate otp then send to the customer."""

    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.OtpSerializer

    def create(self, request, *args, **kwargs):
        """OTP generate and send to the user mobile Number.

        params:
            mobile (str): New user mobile number
            otp_mode(str): otp types such as LOGIN,SIGNUP and FORGOT

        1. Generate OTP
        2. send the otp code

        """
        phone = self.request.data['mobile']
        otp_mode = self.request.data['otp_mode']

        controller = OtpController(logger)

        logger.info('To get a otp for this number:{}'.format(phone))
        otp_obj = controller.get_otp(phone, otp_mode)

        logger.info('To send a otp for this number:{}'.format(phone))
        controller.send_otp(otp_obj, otp_mode)

        logger.info("OTP sent")
        otp_obj.otp = None
        serializer = self.get_serializer(otp_obj)

        return Response(serializer.data)
