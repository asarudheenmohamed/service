"""Endpoint for the return OTP object."""
import random
import logging

import redis

from app.login.lib.otp_controller import *

from .. import lib, models

logger = logging.getLogger(__name__)


class Otpview:
    """Fetch the OTP from redis DB and create otp."""

    def __init__(self, log):
        """Intialized the logger."""
        self.logger = log or logger
        pass

    def create_otp(self, phone):
        """Create otp based on mobile number.

        Args:
         phone(int):user mobile number

        Returns:
            new otp object

        """
        otp = models.OtpList(
            mobile=phone, otp=random.randint(1000, 9999))
        self.logger.info(
            "Generated a new OTP for the number {}".format(phone))
        otp.save()
        return otp

    def get_object(self, phone, type_):
        """Get otp object.

        Args:
         phone(int):user mobile number
         type_(int):otp sent types are forgot otp=1 or signup otp=2

        Returns:
         otp object for that user

        """
        # redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
        redis_db = redis.StrictRedis(
            host="localhost", unix_socket_path='/var/run/redis/redis.sock')

        # check if user exists
        try:
            customer = models.FlatCustomer.load_by_phone_mail(phone)
        except models.CustomerNotFound:
            raise exceptions.PermissionDenied("User does not exits")

        otp = models.OtpList.redis_get(redis_db, phone, type_, 'OTP')
        if otp is None:
            self.logger.debug(
                "Generated a new OTP for the number {}".format(phone))
            otp = self.create_otp(phone)
            models.OtpList.redis_save(redis_db, otp, type_, 'OTP')
        return otp
