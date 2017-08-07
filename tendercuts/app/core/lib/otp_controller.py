"""Endpoint for the return OTP object."""
import logging
import random

from app.core.lib.redis_controller import *
from app.core.lib.user_controller import *
from app.login.lib.otp_controller import *

from .. import lib, models

logger = logging.getLogger(__name__)


class Otpview:
    """Fetch the OTP from redis DB and create otp."""

    def __init__(self, log=None):
        """Intialized the logger."""
        self.logger = log or logger

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

    def get_object(self, phone, otp_type):
        """Get otp object.

        Args:
         phone(int):user mobile number
         type_(int):otp sent types are forgot otp=1 or signup otp=2

        Returns:
         otp object for that user

        """
        # check if user exists
        try:
            customer = CustomerSearchController.load_by_phone_mail(phone)
        except models.CustomerNotFound:
            raise exceptions.PermissionDenied("User does not exits")

        otp = RedisController().redis_get(phone, otp_type)
        if otp is None:
            self.logger.debug(
                "Generated a new OTP for the number {}".format(phone))
            otp = self.create_otp(phone)
            RedisController().redis_save(otp, otp_type)
        return otp

    def otp_verify(self, otp, customer_otp):
        """Verify otp in redis db."""
        if otp.otp == customer_otp:
            RedisController().set(otp.mobile, 'verified')
            status = True
        else:
            status = False

        return status
