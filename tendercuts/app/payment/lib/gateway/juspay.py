"""
Juspay gateway
"""
from __future__ import absolute_import, unicode_literals

import base64
import hashlib
import hmac
import json
import logging
import urllib

import juspay
import requests
from app.core import models as core_models
from app.core.lib.exceptions import OrderNotFound
from django.conf import settings

from ... import models
from .base import AbstractGateway


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

        self.return_url = settings.PAYMENT['JUSPAY']['return_url']
        self.secret = settings.PAYMENT['JUSPAY']['secret']
        self.merchant_id = settings.PAYMENT['JUSPAY']['merchant_id']

    def _juspay_user(self, user_id):
        return "{}_{}".format(self.MAGENTO_CODE, user_id)

    def check_payment_status(self, order_id, vendor_id):
        """
        @override

        params:
            order_id (str): Increment_id
            vendort_id (str): Not used

        returns:
            boolean: indicating if the payment was captured.
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

        # Special hack for stagin mode
        if juspay.environment == "sandbox":
            nbs = nbs * 25

        cards = []
        if user_id:
            cards = juspay.Cards.list(customer_id=self._juspay_user(user_id))

        return [models.PaymentMode.from_justpay(mode) for mode in nbs + cards]

    def juspay_order_create(self, order, customer):
        """
        params:
            order (SalesFlatOrder) - order intance
            customer (juspay.Customer) - customer

        returns:
            juspay.Order
        """
        jp_order = juspay.Orders.create(
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

    def get_or_create_customer(self, user):
        """"
        params:
            user (str or tuple): Can either be str reprsenting the user id
                or a tuple representing (user_id, mail, phone, name)

        returns:
            juspay.User object
        """
        # conversion to tuple
        if isinstance(user, str):
            user = core_models.FlatCustomer.load_basic_info(user)

        user_id = self._juspay_user(user[0])
        self.log.debug("Creating customer in JP with id: {}".format(user_id))

        try:
            cust = juspay.Customers.get(id=user_id)
            self.log.debug(
                "Already exist so fetched the customer from JP with id: {}".format(user_id))
        except Exception:
            # this is so wrong, but Jp has no excpetions in theri library
            cust = juspay.Customers.create(
                # neeed to be 8 chars
                object_reference_id=user_id,
                email_address=user[1],
                mobile_number=user[2],
                first_name=user[3],
                last_name='')   # last name in mandatory
            self.log.debug(
                "Created a customer in JP with id: {}".format(user_id))

        return cust

    def start_transaction(self, payment_mode, save_to_locker=True):
        """
        Performs multiple steps

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

        jp_customer = self.get_or_create_customer(str(order.customer_id))

        self.juspay_order_create(order, jp_customer)

        txn_processor = JuspayTransaction(
            payment_mode,
            jp_customer,
            save_to_locker=save_to_locker)

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


class JuspayTransaction:
    """
    A thin wrapper for the transaction API

    """

    def __init__(self, payment_mode, jp_customer, save_to_locker=True):
        self.payment_mode = payment_mode
        self.jp_customer = jp_customer
        self.merchant_id = settings.PAYMENT['JUSPAY']['merchant_id']
        self.url = settings.PAYMENT['JUSPAY']['url']
        self.save_to_locker = save_to_locker

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

    def process_card(self):
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
            save_to_locker=self.save_to_locker)

        return transaction

    def tokenize_card(self):
        """
        For convenience we are triggering the tokenize request from the server
        instead of the client.

        Also adds the card to the lock if option is enabled

        returns:
            string: A token representing card (no, expiry, )
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
        token = response.json()['token']

        if self.save_to_locker:
            juspay.Cards.create(merchant_id=self.merchant_id,
                                customer_id=self.jp_customer.object_reference_id,
                                customer_email=self.jp_customer.email_address,
                                card_token=response.json()['token'])

        return token

    def _convert_to_url(self, xact):
        """
        DEPRECATED: SINCE we are using SAFEBROWSER we are removing this.

        params:
            xact: Justpay transaction
        """

        authentication = xact.payment.authentication

        if authentication.method == "GET":
            return authentication.url

        url = '<html><head></head><body>'
        url += '<form id="paymentForm" action="{}" method="POST">'.format(
            authentication.url)

        if authentication.params:
            for key in authentication.params:
                url += '<input type="hidden" name="{}" value="{}">'.format(
                    key, authentication.params[key])

        url += '</form>'

        url += '<script type="text/javascript">'
        url += 'document.getElementById("paymentForm").submit();'
        url += '</script>'
        url += '</body></html>'

        page_content = 'data:text/html;base64,' + base64.b64encode(url)

        return page_content

    def process(self):
        """
        Process call to process both card and NB

        returns:
            Juspay Transaction object.

        eg: data:text/html;base64 || url
        """

        transaction = None

        if self.payment_mode.is_juspay_nb():
            transaction = self.process_nb()

        # if its a new card first tokenize it and make it old
        if self.payment_mode.is_juspay_card():

            # if its  a new card then tokenize it first
            if self.payment_mode.is_juspay_card(new_check=True):
                self.payment_mode.gateway_code_level_1 = self.tokenize_card()

            transaction = self.process_card()

        #return self._convert_to_url(transaction)
        return transaction
