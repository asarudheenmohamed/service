"""Payu Gateway APIs."""

from .base import AbstractGateway

from app.payment import models as models
import requests
import hashlib
import json
import logging

from django.conf import settings


class Payu(AbstractGateway):
    """Payu Gateway."""

    SUCCESS = 'success'

    def __init__(self, log=None):
        """Constructor."""
        super(Payu, self).__init__()

        self.merchant_id = settings.PAYMENT['PAYU']['merchant_id']
        self.secret = settings.PAYMENT['PAYU']['secret']
        self.base_url = settings.PAYMENT['PAYU']["url"]

    @property
    def magento_code(self):
        """Magento Code."""
        return "payubiz"

    def check_payment_status(self, order_id):
        """Check the status of order in juspay gateway.

        @override
        params:
            order_id (str) increment_id

        """
        COMMAND = "verify_payment"
        wsUrl = "{}merchant/postservice?form=2".format(self.base_url)

        hash_val = hashlib.sha512("{}|{}|{}|{}".format(
            self.secret,
            COMMAND,
            # "|".join(order_ids),
            order_id,
            self.merchant_id))

        data = {
            'key': self.secret,
            'hash': hash_val.hexdigest(),
            'var1': order_id,
            'command': COMMAND}

        res = requests.post(wsUrl, data=data, timeout=30)
        res.raise_for_status()

        self.log.info("Payu response: {}".format(res.text))

        response = res.json()
        # response = [response] if type(response) is not list else response
        for inc_id, status in response['transaction_details'].items():
            return status.get('status', False) == self.SUCCESS

        return False
