"""Endpoint for user login."""

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
from app.core.lib.user_controller import *

from .. import lib
from .. import models
from .. import serializers
# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserLoginApi(APIView):
    """Enpoint that uses magento API to mark an order as comple."""

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """Authenticate the requestuser.

        params:
            phone/email (str) - Atleast one of the arguments should
                be provided
            password (str)- Password

        returns:
            A User object that is serialized

        """
        username = self.request.data.get(
            'email', None) or self.request.data['phone']
        password = self.request.data.get('password',False)
        otp_mode = self.request.data.get('otp_mode',False)
        user = None
        try:
            logger.info("the user authenticate by {} ".format(otp_mode))
            user = CustomerController.authenticate(
                username, password, otp_mode)
            user.message = 'success'

            logger.debug("Logging successful for user {}".format(username))

        except CustomerNotFound:
            user = CustomerController(None)
            user.message = "User does not exists!"

            logger.warn("user {} not found".format(username))

            return Response(user.message)

        except InvalidCredentials:
            user = CustomerController(None)
            user.message = "Invalid username/password"

            logger.warn(
                "user {} tried to login with invalid details".format(username))

            return Response(user.message)

        except ValueError:
            user = CustomerController(None)
            user.message = "your otp is not verified"
            return Response(user.message)

        except Exception as e:
            user = CustomerController(None)
            user.message = "Invalid username/password"
            exception = traceback.format_exc()

            logger.error("user {} tried to login caused and exception {}".format(
                username,
                exception))
        # Todo: Optimize and use flat
        return Response(user.deserialize())
