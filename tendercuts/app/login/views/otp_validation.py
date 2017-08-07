"""This module is deprecated."""
import logging
import random
import string
import traceback

import redis
from django.http import Http404
from rest_framework import exceptions, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .. import lib, models
import app.core.lib.magento as magento
from app.core.lib.communication import SMS
from app.core.lib.otp_controller import *

from .. import lib, models, serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OtpValidation(APIView):
    """OTP Validation."""

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        """OTP validate in signup,forgot password and login method.

        params:
            mobile (str): New user mobile number
            type(int):otp types are forgot otp or signup otp

        Returns:
            Otp validation status

        """
        type_ = self.request.GET.get('type')
        customer_otp = self.request.GET.get('otp')
        phone = kwargs['mobile']

        otp_obj = Otpview(logger)
        # get otp object
        otp = otp_obj.get_object(phone, type_)
        # verify the otp
        otp_validation = otp_obj.otp_verify(otp, customer_otp)

        if otp_validation == True:
            message = 'succesfuly verified'
        else:
            message = 'Your OTP is Invalid'

        return Response(
            {'status': otp_validation,
             'message': message})
