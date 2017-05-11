"""
Juspay gateway
"""
from __future__ import absolute_import, unicode_literals
import juspay
from django.conf import settings

from app.core.lib.exceptions import OrderNotFound
from app.core import models as core_models

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
        self.log.debug("Checking order status for {} from JUSPAY".format(order_id))
        # response = juspay.Orders.status(order_id=order_id)
        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)

        if not order:
            raise OrderNotFound()

        order = order[0]
        self.log.debug("Order status for {} is {}".format(order_id, order.status))

        return order.status == 'pending' or order.status == "scheduled_order"
