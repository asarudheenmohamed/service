"""Endpoint for the otp creation and otp validation."""
import logging
import random

from rest_framework import exceptions

from app.core.lib.user_controller import (CustomerSearchController,
                                          RedisController)

from .. import models

logger = logging.getLogger(__name__)


class OtpController(object):
    """Fetch the OTP from redis DB and create otp and otp validation."""

    RESET_PASSWORD = 'RESET_PASSWORD'
    LOGIN = 'LOGIN'
    SIGNUP = 'SIGNUP'
    FORGOT = 'FORGOT'

    def __init__(self, log=None):
        """Intialized Redis Controller."""
        self.logger = log or logger
        self.redis = RedisController()

    def create_otp(self, phone):
        """Create otp based on mobile number.

        Args:
         phone(int):user mobile number

        Returns:
            new otp object

        """
        otp = models.OtpList(
            mobile=phone,
            otp=random.randint(1000, 9999))
        otp.save()

        self.logger.info(
            "Generated a new OTP for the number {}".format(phone))

        return otp

    def get_otp(self, phone, otp_type):
        """Get otp object.

        Args:
         phone(int): User mobile number.
         otp_type(int): Otp sent types are forgot or signup or login.

        Returns:
         otp object for that user

        """
        # check if user exists
        try:
            CustomerSearchController.load_by_phone_mail(phone)
        except models.CustomerNotFound:
            raise exceptions.PermissionDenied("User does not exits")

        key = "{}:{}".format(otp_type, phone)
        otp = self.redis.get_key(key)

        if otp is None:
            self.logger.debug(
                "Generated a new OTP for the number {}".format(phone))
            otp = self.create_otp(phone)
            key = "{}:{}".format(otp_type, otp.mobile)
            self.redis.set_key(key, otp.otp)

        else:
            otp = models.OtpList(mobile=phone, otp=otp)

        return otp

    def otp_verify(self, otp, customer_otp):
        """Verify otp in redis db."""
        if otp.otp == customer_otp:
            self.redis.set_key(otp.mobile, 'verified')
            status = True
        else:
            status = False

        return status
