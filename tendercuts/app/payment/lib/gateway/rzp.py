"""
Razorpay PG
"""

import logging

import razorpay
from django.conf import settings

from app.core.lib.exceptions import OrderNotFound

from ... import models
from .base import AbstractGateway


class RzpGateway(AbstractGateway):
    """
    Rzp implementation
    """
    SUCCESS = "paid"

    def __init__(self, log=None):
        super(self.__class__, self).__init__()
        api_key = settings.PAYMENT['RZP']['id']
        api_secret = settings.PAYMENT['RZP']['secret']
        self.log.info("Initializing RZP with key {} and secret{}".format(
            api_key, api_secret))
        self.client = razorpay.Client(auth=(api_key, api_secret))

    def check_payment_status(self, order_id, vendor_id):
        """
        params:
            order_id: increment_id
        """
        self.log.debug("Checking payment status for id {} and vendorid: {}".format(
            order_id, vendor_id))
        response = self.client.order.fetch(order_id=vendor_id)

        self.log.debug("Got response: {}".format(response))
        return response['status'] == self.SUCCESS
