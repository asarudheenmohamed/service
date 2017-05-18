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

from . import lib
from . import models
from . import serializers

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
        fields = ['reward_points', 'store_credit', 'address']

        if username is None:
            raise exceptions.ValidationError("Invalid user")

        attributes = []

        try:
            user = models.FlatCustomer.load_by_phone_mail(username)
            logger.debug("Fetched user data {} for {} successfully".format(
                username, user.__dict__))

            for f in fields:
                attributes.append({
                    "code": f,
                    "value": user._flat[f]
                })

        except Exception as e:
            exception = traceback.format_exc()
            logger.error("user {} tried to fetch data caused and exception {}".format(
                username,
                exception))
            raise exceptions.ValidationError("Invalid user")

        return Response({"attribute": attributes})
