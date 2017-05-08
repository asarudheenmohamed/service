import base64
import hashlib
import hmac
import logging
import urllib

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .lib import gateway as gw
import traceback

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VerifyTransaction(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    GW_MAP = {
        "getsimpl": gw.GetSimplGateway,
        "juspay": gw.JusPayGateway,
        "razorpay": gw.RzpGateway
    }

    def post(self, request, format=None):
        """
        Check the gw code and trigger the appropriate gw action.
        """
        increment_id = self.request.data['increment_id']
        vendor_id = self.request.data.get('vendor_id', None)
        gateway = self.request.data.get('gw', None)

        if gateway not in self.GW_MAP:
            raise exceptions.ValidationError(('Invalid data'))

        gateway = self.GW_MAP[gateway](log=logger)

        try:
            logger.info("Making payment with {} for the order Is: {}".format(
                gateway, increment_id))
            status = gateway.verify_transaction(
                order_id=increment_id, vendor_id=vendor_id)
            return Response({"status": status})
        except Exception as e:
            exception = traceback.format_exc()
            logger.info("Payemnt failed for {} with error {}".format(
                increment_id, str(exception)))
            return Response({"status": False})


class JusPayApprovalCallBack(APIView):
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
        key = self.__class__.SECRET
        # params := key/value dictionary except `signature`
        #           and `signature_algorithm`
        # signature := "5ctBJ0vURSTS9awUhbTBXCpUeDEJG8X%252B6c%253D"
        # signature_algorithm := "HMAC-SHA256"

        params = request.query_params.dict()
        hash_code = urllib.quote_plus(params.pop("signature"))
        hash_algo = params.pop("signature_algorithm")

        encoded_sorted = []
        for i in sorted(params.keys()):
            encoded_sorted.append(urllib.quote_plus(i) + '=' +
                                  urllib.quote_plus(params.get(i)))

        encoded_string = urllib.quote_plus('&'.join(encoded_sorted))
        dig = hmac.new(key,
                       msg=encoded_string,
                       digestmod=hashlib.sha256).digest()

        computed_hash = urllib.quote_plus(base64.b64encode(dig).decode())
        is_match = computed_hash == hash_code
        
        logger.debug("Trying to verify signature {} and computed signature {}".format(
                computed_hash, hash_code))

        if not is_match:
            raise exceptions.PermissionDenied()

        payment_status = request.query_params['status']
        is_charged =  payment_status == "CHARGED"
        increment_id = request.query_params['order_id']
        
        logger.debug("Trying to approve {} with statu: {}".format(
                increment_id, payment_status))

        if not is_charged:
            return Response({"status": False})

        gateway = gw.JusPayGateway(log=logger)
        try:
            logger.info(
                "confirming payment for the order ID: {}".format(increment_id))
            status = gateway.update_order_status(increment_id)
            return Response({"status": True})
        except Exception as e:
            exception = traceback.format_exc()
            logger.info("JP Payement verification for {} with error {}".format(
                increment_id, str(exception)))
            return Response({"status": False})
