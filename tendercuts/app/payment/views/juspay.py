"""
Just pay related API calls
"""

import logging
import traceback
import urllib

from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from rest_framework import exceptions
from rest_framework import views, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .. import serializer
from ..lib import gateway as gw
from app.core.models import SalesFlatOrder
from app.payment import tasks
from datetime import datetime, timedelta

# Get an instance of a logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
def juspay_webhook(request):
    """Process webhook callbacks"""

    # dirty hack
    # TODO: Needs to be moved to django auth/groups.
    if not request.user.groups.filter(name="Admin").exists():
        return Response({'error': 'Unauthorized'}, status=401)

    gateway = gw.JusPayGateway(log=logger)
    gateway.reconcile_transaction(request.data)

    return Response()


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def juspay_done(request):
    """
    A NOOP callback to act as a end url of the juspay callback flow
    """
    params = request.query_params.dict()

    # if mobile then nuke it
    if params['medium'] != settings.ORDER_MEDIUM['NEW_WEBSITE']:
        return Response()

    order_id = params['increment_id']
    if params['status'] is True:
        url = "{}{}".format(
            settings.PAYMENT['JUSPAY']['web_success_url'],
            order_id
        )
        return HttpResponseRedirect(url)

    url = "{}{}".format(
        settings.PAYMENT['JUSPAY']['web_failure_url'],
        order_id
    )
    return HttpResponseRedirect(url)


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
        GET request for verifying the transactiono

        The reponse is a redirection to the NOOP endpoint which acts as an
        endpoint for the transaction.
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

        sale_order = SalesFlatOrder.objects.filter(increment_id=increment_id)
        sale_order = sale_order.first() # type: SalesFlatOrder

        # Params to push to next request.
        params = {'increment_id': sale_order.increment_id,
                  'medium': sale_order.medium}

        logger.debug("Trying to approve {} with status: {}".format(
            increment_id, payment_status))

        params.update({'status': True})
        success_url = "{}?{}".format(
            reverse('juspay_done', request=request), urllib.urlencode(params))

        params.update({'status': False})
        failure_url = "{}?{}".format(
            reverse('juspay_done', request=request), urllib.urlencode(params))

        if not is_charged:
            return HttpResponseRedirect(failure_url)
            # Response({"status": False})

        try:
            logger.info(
                "confirming payment for the order ID: {}".format(increment_id))
            status = gateway.update_order_status(increment_id)
            logger.info(
                "confirmed payment for the order ID: {} with status {}".format(
                    increment_id, status))

            return HttpResponseRedirect(success_url)
        except Exception as e:
            exception = traceback.format_exc()
            logger.info("JP Payement verification for {} with error {}".format(
                increment_id, str(exception)))

            return HttpResponseRedirect(failure_url)


class PaymentMethodViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    A viewset that provides default `list()` actions.

    TODO: clean me, this shouldn't be a PaymentMethodViewSet, instead a
    separate API. Making changes to this will break all existing customer
    apps. So holding the changes for now.
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

        # if wallets are requested then fetch
        wallets = False
        if "wallets" in self.request.GET:
            wallets = True

        return gateway.fetch_payment_modes(user_id, wallets=wallets)

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

        data = {
            "url": transaction.payment.authentication.url,
            "method": transaction.payment.authentication.method,
            "params": transaction.payment.authentication.params,
            "amount": transaction.amount,
            "txn_id": transaction.txn_id,
            "order_id": transaction.order_id,
            "customer_id": transaction.customer_id,
            "customer_email": transaction.customer_email,
            "customer_phone": transaction.customer_phone
        }
        logger.debug("Sending back {}".format(data))

        return Response(data)
