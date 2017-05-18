"""
Razorpay PG
"""

import logging

import razorpay
from django.conf import settings

from app.core.lib.exceptions import OrderNotFound
from app.core import models as core_models

from ... import models
from .base import AbstractGateway


class RzpGateway(AbstractGateway):
    """
    Rzp implementation
    """
    SUCCESS = "captured"

    def __init__(self, log=None):
        super(self.__class__, self).__init__()
        api_key = settings.PAYMENT['RZP']['id']
        api_secret = settings.PAYMENT['RZP']['secret']
        self.log.info("Initializing RZP with key {} and secret{}".format(
            api_key, api_secret))
        self.client = razorpay.Client(auth=(api_key, api_secret))

    @property
    def magento_code(self):
        return "razorpay"

    def check_payment_status(self, order_id, vendor_id):
        """
        params:
            order_id: increment_id
        """
        self.log.debug("Checking payment status for id {} and vendorid: {}".format(
            order_id, vendor_id))
        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)

        if not order:
            raise OrderNotFound()

        response = self.client.payment.capture(
            vendor_id,
            int(order[0].grand_total * 100))  # in paise

        self.log.debug("Got response: {}".format(response))
        return response['status'] == self.SUCCESS
