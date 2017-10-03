"""Endpoint for the otp creation and otp validation."""
import logging
import random

from django.conf import settings
from rest_framework import exceptions

from app.core.lib import cache
from app.core.lib.exceptions import CustomerNotFound
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.communication import SMS
from app.core import models

logger = logging.getLogger(__name__)


class OtpController(object):
    """Fetch the OTP from redis DB and create otp and otp validation."""

    RESET_PASSWORD = 'RESET_PASSWORD'
    LOGIN = 'LOGIN'
    SIGNUP = 'SIGNUP'
    FORGOT = 'FORGOT'

    msg_content = {
        'FORGOT': "as your OTP to reset your password.",
        'SIGNUP': "as your signup OTP. OTP is confidential.",
        'LOGIN': "as your login OTP. OTP is confidential."}

    def __init__(self, log=None):
        """Intialized Redis Controller."""
        self.logger = log or logger

    def _generate_redis_key(self, phone, otp_type):
        """Generate the save key."""
        return "{}:{}".format(otp_type, phone)

    def _create_otp(self, phone, otp_type):
        """Create otp based on mobile number.

        Params:
            phone(int): user mobile number

        Returns:
            A new OTP value (int)

        """
        key = self._generate_redis_key(phone, otp_type)
        otp = random.randint(1000, 9999)
        a = cache.set_key(key, otp, 60 * 15)
        self.logger.info(
            "Generated a new OTP for the number {}".format(phone))

        return otp

    def send_otp(self, otp_obj, otp_mode):
        """Send Otp to a customer."""
        msg = ("""Use {} {}.""").format(
            otp_obj.otp, self.msg_content[str(otp_mode)])
        SMS().send_otp(
            phnumber=otp_obj.mobile,
            message=msg,
            otp=otp_obj.otp)

    def get_otp(self, phone, otp_type):
        """Get otp object.

        Args:
         phone(int): User mobile number.
         otp_type(str): Otp sent types are forgot or signup or login.

        Returns:
         otp object for that user

        """
        # check if user exists
        if otp_type != OtpController.SIGNUP:
            try:
                CustomerSearchController.load_by_phone_mail(phone)
            except CustomerNotFound:
                raise exceptions.PermissionDenied("User does not exists")

        key = self._generate_redis_key(phone, otp_type)
        self.logger.info(
            'get otp for the redis db in this mobile mumber {}'.format(phone))
        otp = cache.get_key(key)
        # Create a new one
        if len(str(otp)) == 1 or otp is None:
            self.logger.debug(
                "Generated a new OTP for the number {}".format(phone))
            otp = self._create_otp(phone, otp_type)

        otp = models.OtpList(mobile=phone, otp=otp)

        return otp

    def otp_verify(self, otp, customer_otp):
        """Verify otp in redis db."""

        status = (int(otp.otp) == int(customer_otp))

        if status:
            cache.set_key(otp.mobile, 'verified', 60 * 10)
            self.logger.info('The otp will be verified')

        return status
