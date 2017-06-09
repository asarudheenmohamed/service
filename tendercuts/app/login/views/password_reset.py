"""
Endpoints to provide password reset
"""

# Create your views here.magent
# import the logging library
import logging
import random
import string

import redis
from app.core.lib.communication import SMS
from rest_framework import exceptions, viewsets
from rest_framework.response import Response

from .. import  models, serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpForgotPasswordApiViewSet(viewsets.GenericViewSet):
    """
    OTP for resetting password
    TODO: EXTREMELY HACKY
    """
    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        """
        params:
            mobile (str): Phone number to generate an OTP
            resend (str): Resend type sending otp type

        1. Generate OTP/ get existin OTP, which is valid for 15 mins
        2. send the code
        3. resend OTP/ types are voice or text

        If the customer is not available then thrown an error
        """
        # redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
        redis_db = redis.StrictRedis(
            host="localhost", unix_socket_path='/var/run/redis/redis.sock')

        phone = kwargs['mobile']
        resend = self.request.GET.get('resend_type', None)
        # check if user exists
        try:
            customer = models.FlatCustomer.load_by_phone_mail(phone)
        except models.CustomerNotFound:
            raise exceptions.PermissionDenied("User does not exits")

        otp = models.OtpList.redis_get(redis_db, phone)
        if otp is None:
            otp = models.OtpList(
                mobile=phone,
                otp=random.randint(1000, 9999))
            models.OtpList.redis_save(redis_db, otp)
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
        """
        1. Fetch the OTP from redis DB and validate the OTP
        2. Then go ahead and reset the password!

        """
        #redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
        redis_db = redis.StrictRedis(
            host="localhost", unix_socket_path='/var/run/redis/redis.sock')

        phone = self.request.data['mobile']
        otp = self.request.data['otp']
        dry_run = self.request.data.get('dry_run', False)

        otp_object = models.OtpList.redis_get(redis_db, phone)

        if otp_object is None or otp_object.otp != otp:
            raise exceptions.ValidationError("Invalid OTP")

        random_pass = ''.join(
            [random.choice(string.ascii_lowercase) for n in xrange(5)])
        random_pass += str(random.randint(0, 9))

        msg = ("""Your request for password reset is now successful. New password: {}""").format(
            random_pass)
        SMS().send(phnumber=phone, message=msg)

        customer = models.FlatCustomer.load_by_phone_mail(phone)
        customer.reset_password(random_pass, dry_run=dry_run)

        otp_object.otp = None
        serializer = self.get_serializer(otp_object)

        return Response(serializer.data)
