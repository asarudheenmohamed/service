"""Summary

Attributes:
    logger (TYPE): Description
"""
# Create your views here.magent
# import the logging library
import logging
import random
import string
import traceback

import redis
from django.http import Http404
from rest_framework import exceptions, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

import app.core.lib.magento as magento
from app.core.lib.communication import SMS
from app.core.lib.user_controller import *

from . import lib, models, serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserDataFetch(APIView):
    """
    user/fetch : Gets the user profile data
    """

    def get(self, request, format=None):
        """
        Args:
            request :
                Get params:
                1. email/phone (str): Check if user exists

        Raises:
            exceptions.ValidationError: Raises an exception in
            case not valid user if found
        """
        username = self.request.GET.get('email', None) or \
            self.request.GET.get('phone', None)
        fields = ['reward_points', 'store_credit', 'address','default_shipping','default_billing']

        if username is None:
            raise exceptions.ValidationError("Invalid user")

        attributes = []

        try:
            user = CustomerSearchController.load_by_phone_mail(username)
            logger.debug("Fetched user data {} for {} successfully".format(
                username, user.__dict__))

            for f in fields:
                attributes.append({
                    "code": f,
                    "value": user._flat[f]
                })
        
        except KeyError:
            attributes.append({
                "code": f,
                "value": {}
            })

        except:
            exception = traceback.format_exc()
            logger.error("user {} tried to fetch data caused and exception {}".format(
                username,
                exception))
            raise exceptions.ValidationError("Invalid user")

        return Response({"attribute": attributes})
