# Create your views here.magent
import redis
import app.core.lib.magento as magento
from . import lib
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics, mixins, exceptions
from app.core.lib.communication import SMS
from django.http import Http404
import random
import string
# import the logging library
import logging
import traceback

# Get an instance of a logger
logger = logging.getLogger(__name__)
from .lib import gateway as gw


class SimplClaimTxnApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """

    def post(self, request, format=None):
        """
        """
        increment_id = self.request.data['increment_id']
        token = self.request.data['token']

        simpl = gateway.GetSimplGateway()
        status = simpl.update_order_with_payment(
            increment_id,
            token)

        return Response({"status": status})
