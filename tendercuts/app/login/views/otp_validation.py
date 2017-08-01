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


class OtpValidation(viewsets.GenericViewSet):
    """OTP Validation."""

    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
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

        redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
        # redis_db = redis.StrictRedis(
        #     host="localhost", unix_socket_path='/var/run/redis/redis.sock')
        otp_obj = Otpview(logger)
        otp = otp_obj.get_object(phone, type_)

        if otp.otp == customer_otp:
            models.OtpList.redis_key_value_save(
                redis_db, otp.mobile, 'verified')
            status = True
            message = 'succesfuly verified'
        else:
            status = False
            message = "Invalid your OTP"
            # raise exceptions.ValidationError("Invalid OTP")
        return Response({'status': status, 'message': message})
