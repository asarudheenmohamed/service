"""Endpoints to provide password reset."""

# Create your views here.magent
# import the logging library
import logging
import random
import string

from rest_framework import exceptions, viewsets
from rest_framework.response import Response

from app.core.lib.communication import SMS
from app.core.lib.otp_controller import OtpController
from app.core.lib.redis_controller import RedisController
from app.core.lib.exceptions import CustomerNotFound, InvalidCredentials
from app.core.lib.user_controller import (CustomerController,
                                          CustomerSearchController)

from .. import models, serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpForgotPasswordApiViewSet(viewsets.GenericViewSet):
    """OTP for resetting password."""
    
    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        """Return the serializer data of otp object.

        params:
            mobile (str): Phone number to generate an OTP
            resend (str): Resend type sending otp type

        1. Generate OTP/ get existin OTP, which is valid for 15 mins
        2. send the code
        3. resend OTP/ types are voice or text

        If the customer is not available then thrown an error

        """
        phone = kwargs['mobile']
        resend = self.request.GET.get('resend_type', None)
        # check if user exists
        otp_obj = OtpController(logger)
        otp = otp_obj.get_otp(phone, otp_obj.FORGOT)

        logger.info("Generating OTP for {} with code: {}".format(
            otp.mobile, otp.otp))
        msg = ("""Use {} as your OTP to reset your password.""").format(otp.otp)

        SMS().send_otp(
            phnumber=otp.mobile, message=msg, otp=otp.otp, resend_type=resend)
        logger.info("OTP sent")

        otp.otp = None
        serializer = self.get_serializer(otp)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Fetch the OTP from redis DB and validate the OTP.

        1.Then go ahead and reset the password!

        """
        phone = self.request.data['mobile']
        customer_otp = self.request.data.get('otp', False)
        dry_run = self.request.data.get('dry_run', False)

        otp_obj = OtpController(logger)
        otp = otp_obj.get_otp(phone, otp_obj.FORGOT)

        if customer_otp:
           otp_validation = otp_obj.otp_verify(otp, customer_otp)
           if not otp_validation:
             raise exceptions.ValidationError("Invalid OTP")
        else:
            redis_value = RedisController().get_key(phone)
            if redis_value not in ['verified']:
                raise InvalidCredentials

        random_pass = ''.join(
            [random.choice(string.ascii_lowercase) for n in xrange(5)])
        random_pass += str(random.randint(0, 9))

        customer = CustomerSearchController.load_by_phone_mail(phone)
        CustomerController(
            customer.customer).reset_password(
            random_pass,
            dry_run=dry_run)
        msg = ("""Your request for password reset is now successful. New password: {}""").format(
            random_pass)

        SMS().send(phnumber=phone, message=msg)

        otp.otp = None
        serializer = self.get_serializer(otp)

        return Response(serializer.data)
