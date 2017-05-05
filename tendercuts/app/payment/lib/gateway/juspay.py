"""
Juspay gateway
"""
from __future__ import absolute_import, unicode_literals
import juspay
from django.conf import settings

from .base import AbstractGateway


class JusPayGateway(AbstractGateway):
    """
    JusPay integration
    """
    SUCCESS = "CHARGED"

    def __init__(self, log=None):
        super(JusPayGateway, self).__init__()
        juspay.api_key = settings.PAYMENT['JUSPAY']['id']
        juspay.environment = settings.PAYMENT['JUSPAY']['environment']

    def check_payment_status(self, order_id, vendor_id):
        """
        params:
            order_id (str): Increment_id
            vendort_id (str): Not used
        """
        self.log.debug("Checking order status from JUSPAY")
        response = juspay.Orders.status(order_id=order_id)

        if response:
            self.log.debug("Response from server: {}".format(response.status))
        return response.status == self.SUCCESS
