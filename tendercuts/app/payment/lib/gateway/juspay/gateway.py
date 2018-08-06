"""
Juspay gateway
"""
from __future__ import absolute_import, unicode_literals

import base64
import hashlib
import hmac
import traceback
import urllib
from datetime import datetime, timedelta

import pytest

from app.core import models as core_models
from app.core.lib.exceptions import OrderNotFound, send_exception
from app.core.lib.user_controller import *
from app.payment import tasks

from .... import models
from ..base import AbstractGateway
from .customer import JuspayCustomer
from .mixin import JuspayMixin
from .transaction import JuspayTransaction
from .webhook import JuspayOrderSuccessProcessor


@pytest.mark.django_db
class JusPayGateway(AbstractGateway, JuspayMixin):
    """JusPay integration."""

    NETBANKING_CODE = "NB"
    WALLET_CODE = "WALLET"
    SUCCESS = "CHARGED"

    def __init__(self, log=None):
        super(JusPayGateway, self).__init__()

    # @property
    # def magento_code(self):
    #     return "juspay"

    # def _juspay_user(self, user_id):
    #     return "{}_{}".format(self.magento_code, user_id)

    def claim_payment(self, order_id, vendor_id):
        """Transaction is already claimed from callback, so we do local check.

        @override

        params:
            order_id (str): Increment_id
            vendort_id (str): Not used

        returns:
            boolean: indicating if the payment was captured.

        """
        # response = juspay.Orders.status(order_id=order_id)
        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)

        if not order:
            raise OrderNotFound()

        order = order[0]
        self.log.debug("VERIFY: Order status for {} is {}".format(
            order.increment_id, order.status))

        is_paid = order.status == 'pending' or order.status == "scheduled_order"

        if is_paid:
            return is_paid

        # If the order is not paid then, double check at pg
        juspay_order = self.juspay.Orders.status(order_id=order.increment_id)
        self.log.debug( "Order status for {} from JUSPAY is {}".format(
            order_id, juspay_order.status))

        if juspay_order.status == "CHARGED":
            return True

        return False

    def verify_signature(self, params, hash_code, hash_algo):
        """Verify the HASH signature.

        params:
            params: List of all params from the callback except signature and
                    algo
            hash_code(str): Computed hash
            hash_algo (str): Algorithm used to generate signature

        returns:
            boolean

        # params := key/value dictionary except `signature`
        #           and `signature_algorithm`
        # signature := "5ctBJ0vURSTS9awUhbTBXCpUeDEJG8X%252B6c%253D"
        # signature_algorithm := "HMAC-SHA256"

        """
        # Sort the parms after encoding them
        encoded_sorted = []
        for i in sorted(params.keys()):
            encoded_sorted.append(urllib.quote_plus(i) + '=' +
                                  urllib.quote_plus(params.get(i)))

        encoded_string = urllib.quote_plus('&'.join(encoded_sorted))
        dig = hmac.new(self.secret,
                       msg=encoded_string,
                       digestmod=hashlib.sha256).digest()

        computed_hash = urllib.quote_plus(base64.b64encode(dig).decode())

        return computed_hash == hash_code

    def fetch_payment_modes(self, user_id=None, wallets=False):
        """Get all possible payment modes including user's saved card details.

        params:
            user_id: User id from whom saved cards should be specified

        returns:
            [PaymentMode]

        """
        modes = self.juspay.Payments.get_payment_methods(
            merchant_id=self.merchant_id)

        nbs = [mode for mode in modes
               if mode.payment_method_type == self.NETBANKING_CODE]

        # Special hack for stagin mode
        if self.juspay.environment == "sandbox":
            nbs = nbs * 25

        cards = []
        if user_id:
            cards = self.juspay.Cards.list(
                customer_id=JuspayCustomer.get_user_id(user_id))

        wallet_list = []
        if wallets:
            wallet_list = [mode for mode in modes
                           if mode.payment_method_type == self.WALLET_CODE]

        return [models.PaymentMode.from_justpay(
            mode) for mode in nbs + cards + wallet_list]

    def juspay_order_create(self, order, customer):
        """First create an order in Juspay.

        params:
            order (SalesFlatOrder) - order intance
            customer (juspay.Customer) - customer

        returns:
            juspay.Order

        """
        jp_order = self.juspay.Orders.create(
            order_id=order.increment_id,
            amount=order.grand_total,
            currency='INR',
            # not ID but object reference ID which is juspay_18963 ID
            customer_id=customer.object_reference_id,
            customer_email=customer.email_address,
            customer_phone=customer.mobile_number,
            return_url=self.return_url,
            # RZP needs a fucking description field
            description=order.increment_id)

        return jp_order

    def start_transaction(self, payment_mode, save_to_locker=True):
        """Start the transaction, Performs multiple steps.

        0. Fetch the mage order
        1. fetch the customer/create the customer
        2. Creates an order in JP
        3. for that order creates a transaction using the payment mode

        params:
            payment_mode(PaymentMode) - mode to use for payment

        returns:
            juspay.Transaction

        """
        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=payment_mode.order_id)

        if not order:
            raise OrderNotFound()

        order = order[0]

        jp_customer = JuspayCustomer(self.log).get_or_create_customer(
            str(order.customer_id))

        self.juspay_order_create(order, jp_customer)

        txn_processor = JuspayTransaction(
            payment_mode,
            jp_customer,
            save_to_locker=payment_mode.persist)

        txn = txn_processor.process()

        # HACK this is directly sent out of the API layer, but a transaction
        # model without amount doesn't make sense so we tag along the grand total
        # also customer details
        # TODO: Need to move it to model someday!!
        txn.amount = order.grand_total
        txn.customer_id = jp_customer.object_reference_id,
        txn.customer_email = jp_customer.email_address
        txn.customer_phone = jp_customer.mobile_number

        return txn

    def check_payment_status(self, order_id):
        """Check the status of order in juspay gateway.

        @override
        params:
            order_id (str) increment_id

        """
        juspay_order = self.juspay.Orders.status(order_id=order_id)
        return juspay_order.status == self.SUCCESS if juspay_order else False

    def reconcile_transaction(self, payload):
        """Order success trigger in celery tasks.
        Params:
            payload(dict):order juspay dict obj
            eta: task execution time
        """
        content = payload.get('content', {})
        order = content.get('order', {})
        order_id = order.get('order_id', None)
        eta_time = datetime.utcnow() + timedelta(seconds=60)

        if payload['event_name'] == "ORDER_SUCCEEDED":
            # Set task execution time
            tasks.order_success.apply_async(args=[order_id], eta=eta_time)
