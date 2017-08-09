"""This module is deprecated."""
import logging
import random
import string

from rest_framework import viewsets
from rest_framework.response import Response

from app.core.lib.communication import SMS
from app.core.lib.otp_controller import OtpController
from app.core.lib.user_controller import (CustomerController,
                                          CustomerSearchController)

from .. import models, serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpApi(viewsets.GenericViewSet):
    """OTP resend for Signup method."""

    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        """OTP send for user mobile CustomerControllerNumber.

        params:
            mobile (str): New user mobile number
            resend (str): OTP resend type for text ot voice method
            type(int):otp types are forgot otp or signup otp

        1. Generate OTP
        2. send the otp code
        3. resend OTP/ types are voice or text

        """
        msg_content = {
            'FORGOT': "as your OTP to reset your password.",
            'SIGNUP': "as your signup OTP. OTP is confidential.",
            'LOGIN': "as your login OTP. OTP is confidential."}
        phone = kwargs['mobile']
        resend = self.request.GET.get('resend_type', None)
        otp_type = self.request.GET.get('otp_type')

        otp_obj = OtpController(logger)
        otp = otp_obj.get_otp(phone, otp_type)

        msg = ("""Use {} {}.""").format(otp.otp, msg_content[str(otp_type)])
        SMS().send_otp(
            phnumber=otp.mobile,
            message=msg,
            otp=otp.otp,
            resend_type=resend)

        logger.info("OTP sent")
        otp.otp = None
        serializer = self.get_serializer(otp)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Fetch the OTP from redis DB and validate the OTP.

        1.Then go ahead and reset the password!

        """
        phone = self.request.data['mobile']
        customer_otp = self.request.data['otp']
        dry_run = self.request.data.get('dry_run', False)

        otp_obj = OtpController(logger)
        otp_object = otp_obj.get_otp(phone, otp_obj.RESET_PASSWORD)
        otp_validation = otp_obj.otp_verify(otp_object, customer_otp)

        if not otp_validation:
            return Response('Your otp is Invalid.')
        random_pass = ''.join(
            [random.choice(string.ascii_lowercase) for n in xrange(5)])
        random_pass += str(random.randint(0, 9))

        msg = ("""Your request for password reset is now successful. New password: {}""").format(
            random_pass)
        SMS().send(phnumber=phone, message=msg)

        customer = CustomerSearchController.load_by_phone_mail(phone)
        CustomerController(
            customer.customer).reset_password(
            random_pass,
            dry_run=dry_run)

        otp_object.otp = None
        serializer = self.get_serializer(otp_object)

        return Response(serializer.data)
