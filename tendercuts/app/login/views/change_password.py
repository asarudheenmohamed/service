"""
API endpoint for change password
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
from app.core.lib.user_controller import *

from . import lib
from . import models
from . import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserChangePassword(APIView):
    """
    API view to change password. Ideally this should be part of user
    fetch class, since we dont have a serializer yet we will have a different view
    """

    def get_user_id(self):
        """
        Get the user id from the request
        username contains u:18963 => 18963 is the magento IDS
        """
        user = self.request.user
        user_id = user.username.split(":")

        if len(user_id) < 1:
            user_id = None
        else:
            user_id = user_id[1]

        return user_id

    def post(self, request, format=None):
        """
        Args:
            request :
                post data:
                1. new_password (str): New password of the user

        Raises:
            exceptions.ValidationError: Raises an exception in
            case not valid user if found
        """

        user_id = self.get_user_id()
        new_password = request.data["new_password"]

        if not user_id:
            raise exceptions.ValidationError("Invalid user")

        user = CustomerController.load_by_id(user_id)

        logger.info("Resetting password for the user {}".format(user_id))
        user.reset_password(new_password)

        return Response({"status": True})
