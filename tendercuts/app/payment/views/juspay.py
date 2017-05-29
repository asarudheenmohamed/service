"""
Just pay related API calls
"""

import logging
import traceback
import urllib
import json

from django.conf import settings
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import views, viewsets, mixins

from ..lib import gateway as gw
from .. import serializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class JusPayApprovalCallBack(views.APIView):
    """
    HMAC computation and saving
        [order_id] => 67140
        [status] => AUTHENTICATION_FAILED
        [status_id] => 26
        [signature] => DQ1su1wVQ1D9tYAcPBcAMoG4yagt8+jVLk0Qf/4xg6Y=
        [signature_algorithm] => HMAC-SHA256
    """
    SECRET = settings.PAYMENT['JUSPAY']['secret']
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, **kwargs):
        """
        GET request for verifying the transaction.
        """
        params = request.query_params.dict()
        hash_code = urllib.quote_plus(params.pop("signature"))
        hash_algo = params.pop("signature_algorithm")

        gateway = gw.JusPayGateway(log=logger)
        is_match = gateway.verify_signature(params, hash_code, hash_algo)

        logger.debug("Signature verified status: {}".format(is_match))

        if not is_match:
            raise exceptions.PermissionDenied()

        payment_status = request.query_params['status']
        is_charged = payment_status == "CHARGED"
        increment_id = request.query_params['order_id']

        logger.debug("Trying to approve {} with status: {}".format(
            increment_id, payment_status))

        if not is_charged:
            return Response({"status": False})

        try:
            logger.info(
                "confirming payment for the order ID: {}".format(increment_id))
            status = gateway.update_order_status(increment_id)
            logger.info(
                "confirmed payment for the order ID: {} with status {}".format(increment_id, status))
            return Response({"status": True})
        except Exception as e:
            exception = traceback.format_exc()
            logger.info("JP Payement verification for {} with error {}".format(
                increment_id, str(exception)))
            return Response({"status": False})


class PaymentMethodViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    A viewset that provides default `list()` actions.
    """
    serializer_class = serializer.PaymentModeSerializer

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

    def get_queryset(self):
        """
        Fetches the data from justpay apis
        """
        gateway = gw.JusPayGateway(log=logger)
        user_id = self.get_user_id()

        return gateway.fetch_payment_modes(user_id)

    def create(self, request, *args, **kwargs):
        """
        Initiate the transaction and return the URL
        """
        serialized = serializer.PaymentModeSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        payment_mode = serialized.save()
        logger.debug("Creating a transaction with the following param: {}".format(
            payment_mode.__dict__
        ))

        gateway = gw.JusPayGateway(log=logger)
        transaction = gateway.start_transaction(payment_mode)

        return Response(json.dumps(transaction))



