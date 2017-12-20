from __future__ import absolute_import, unicode_literals

import base64

import requests

from app.core.lib.user_controller import *
from  .mixin import JuspayMixin


class JuspayTransaction(JuspayMixin):
    """
    A thin wrapper for the transaction API

    """

    def __init__(self, payment_mode, jp_customer, save_to_locker=True):
        self.payment_mode = payment_mode
        self.jp_customer = jp_customer
        self.url = settings.PAYMENT['JUSPAY']['url']
        self.save_to_locker = save_to_locker

    def process_nb(self):
        """
        TRigger the NB call and process the order id inside the
        PaymentMode
        """
        transaction = self.juspay.Payments.create_net_banking_payment(
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
        transaction = self.juspay.Payments.create_card_payment(
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
            self.juspay.Cards.create(merchant_id=self.merchant_id,
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

        # return self._convert_to_url(transaction)
        return transaction
