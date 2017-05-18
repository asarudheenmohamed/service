"""
Juspay gateway
"""
from __future__ import absolute_import, unicode_literals

import base64
import hashlib
import hmac
import urllib
import requests
import json

import juspay
from app.core import models as core_models
from app.core.lib.exceptions import OrderNotFound
from django.conf import settings

from .base import AbstractGateway
from ... import models


class JusPayGateway(AbstractGateway):
    """
    JusPay integration
    """
    NETBANKING_CODE = "NB"
    MAGENTO_CODE = "juspay"
    SUCCESS = "CHARGED"

    def __init__(self, log=None):
        super(JusPayGateway, self).__init__()
        juspay.api_key = settings.PAYMENT['JUSPAY']['id']
        juspay.environment = settings.PAYMENT['JUSPAY']['environment']
        self.secret = settings.PAYMENT['JUSPAY']['secret']
        self.merchant_id = settings.PAYMENT['JUSPAY']['merchant_id']

    def check_payment_status(self, order_id, vendor_id):
        """
        params:
            order_id (str): Increment_id
            vendort_id (str): Not used
        """
        self.log.debug(
            "Checking order status for {} from JUSPAY".format(order_id))
        # response = juspay.Orders.status(order_id=order_id)
        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)

        if not order:
            raise OrderNotFound()

        order = order[0]
        self.log.debug("Order status for {} is {}".format(
            order_id, order.status))

        return order.status == 'pending' or order.status == "scheduled_order"

    def verify_signature(self, params, hash_code, hash_algo):
        """
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

    def fetch_payment_modes(self, user_id=None):
        """
        params:
            user_id: User id from whom saved cards should be specified

        returns:
            [PaymentMode]
        """
        modes = juspay.Payments.get_payment_methods(
            merchant_id=self.merchant_id)

        nbs = [mode for mode in modes
               if mode.payment_method_type == self.NETBANKING_CODE]

        cards = []
        if user_id:
            cards = juspay.Cards.list(customer_id=user_id)

        return [models.PaymentMode.from_justpay(mode) for mode in nbs + cards]

    def create_payment(self, payment_mode):
        """
        params:
            order_id (str) - order id that has been created in JUSPAY
            payment_mode(PaymentMode) - mode to use for payment

        returns:
            juspay.Transaction
        """

        return JuspayTransaction(payment_mode).process()


class JuspayTransaction:
    """
    A thin wrapper for the transaction API

    """

    def __init__(self, payment_mode):
        self.payment_mode = payment_mode
        self.merchant_id = settings.PAYMENT['JUSPAY']['merchant_id']
        self.url = settings.PAYMENT['JUSPAY']['url']

    def process_nb(self):
        """
        TRigger the NB call and process the order id inside the
        PaymentMode
        """
        transaction = juspay.Payments.create_net_banking_payment(
            order_id=self.payment_mode.order_id,
            merchant_id=self.merchant_id,
            payment_method_type=self.payment_mode.gateway_code,
            payment_method=self.payment_mode.gateway_code_level_1,  # NB_HDFC
            redirect_after_payment=True,
            format='json')

        return transaction

    def process_card(self, save_to_locker=True):
        """
        Create transaction for credit card

        params:
            save_to_locker (boolean): Saving to JP locker
        """
        transaction = juspay.Payments.create_card_payment(
            order_id=self.payment_mode.order_id,
            merchant_id=self.merchant_id,
            payment_method_type=self.payment_mode.gateway_code,
            card_token=self.payment_mode.gateway_code_level_1,
            # '68d6b0c6-6e77-473f-a05c-b460ef983fd8'
            redirect_after_payment=True,
            format='json',
            card_security_code=self.payment_mode.pin,
            save_to_locker=save_to_locker)

        return transaction

    def tokenize_card(self):
        """
        For convenience we are triggering the tokenize request from the server
        instead of the client.
        """
        data = {
            "merchant_id": self.merchant_id,
            "card_number": self.payment_mode.title,
            "card_exp_year": self.payment_mode.expiry_year,
            "card_exp_month": self.payment_mode.expiry_month,
            "card_security_code": self.payment_mode.pin
        }

        response = requests.post(self.url, data=data)

        # Return the temp token
        return response.json()['token']

    def process(self, save_to_locker=True):
        """
        Process call to process both card and NB

        params:
            save_to_locker (boolean): Saving to JP locker
        """
        if self.payment_mode.is_juspay_nb():
            return self.process_nb()

        # if its a new card first tokenize it and make it old
        if self.payment_mode.is_juspay_card():

            # if its  a new card tehn tokenize it first
            if self.payment_mode.is_juspay_card(new_check=True):
                self.payment_mode.gateway_code_level_1 = self.tokenize_card()

            return self.process_card()
