"""
This module is deprecated
"""
# Create your views here.magent
# import the logging library
import logging
import random
import string
import traceback

import app.core.lib.magento as magento
import redis

from app.core.lib.communication import SMS
from django.http import Http404
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import lib
from .. import models
from .. import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserSignUpApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """

    def post(self, request, format=None):
        """
        """
        email = self.request.data['email']
        phone = self.request.data['phone']
        password = self.request.data['password']
        fullname = self.request.data['name']

        mage = magento.Connector()
        status = mage.api.tendercuts_customer_apis.signup(
            fullname,
            email,
            phone,
            password)

        return Response(status)


class OtpApiViewSet(viewsets.GenericViewSet):
    """OTP resend for Signup method."""
    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        """OTP send for user mobile Number.

        params:
            mobile (str): New user mobile number
            resend (str): OTP resend type for text ot voice method

        1. Generate OTP
        2. send the code
        3. resend OTP/ types are voice or text

        """
        otp = None
        resend = self.request.GET.get('resend_type', None)
        try:
            otp = self.get_object()
            logger.debug(
                "Got an existing OTP for the number {}".format(otp.mobile))
        except Http404:
            otp = models.OtpList(
                mobile=kwargs['mobile'], otp=random.randint(1000, 9999))
            otp.save()
            logger.debug(
                "Generated a new OTP for the number {}".format(otp.mobile))

        msg = ("""Use {} as your signup OTP. OTP is confidential.""").format(otp.otp)
        SMS().send_otp(phnumber=otp.mobile, message=msg, otp=otp.otp, resend_type=resend)

        serializer = self.get_serializer(otp)
        return Response(serializer.data)


class UserExistsApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        """
        """
        email = self.request.GET.get('email', None)
        phone = self.request.GET.get('phone', None)

        user_exists = False
        message = ""

        if email and models.FlatCustomer.is_user_exists(email):
            message = "A user with the same email exists, try Forgot password?"
            user_exists = True
            logger.debug(
                "user already exists for the email user {}".format(email))
        elif phone and models.FlatCustomer.is_user_exists(phone):
            message = "A user with the same phone number exists, try Forgot password?"
            user_exists = True
            logger.debug(
                "user already exists for the phone user {}".format(phone))
        elif phone is None and email is None:
            message = "Invalid data"
            user_exists = True
            logger.debug("invalid credentials as both were none")
        else:
            user_exists = False
            message = ""

        # Todo: Optimize and use flat
        return Response({"result": user_exists, "message": message})
