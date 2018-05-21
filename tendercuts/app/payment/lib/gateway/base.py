"""
Every payment GW should implement this class
"""

from app.core.lib.order_controller import OrderController
from app.core import models as core_models
from app.core.lib import exceptions as core_exceptions
from app.driver import tasks

import abc
import logging


class AbstractGateway(object):
    """
    Base implementation
    """

    def __init__(self, log=None):
        self.log = log or logging.getLogger()

    @abc.abstractproperty
    @property
    def magento_code(self):
        """Payment mehtod name in magento."""
        pass

    @abc.abstractmethod
    def claim_payment(self, order_id, vendor_id):
        """Check the status of the order and claim the payment.

        param:
            order_id (str) increment_id
            vendor_id (str) vendor specific Id

        """
        pass

    @abc.abstractmethod
    def check_payment_status(self, order_id):
        """Check the status of the order in the PG.

        param:
            order_id (str) increment_id

        """
        pass

    def reconcile_transaction(self, payload):
        """Triggered after sometime, mostly from webhooks or polling.
        Optional method.

        param:
            payload (dict) response json from the gateway.

        """
        pass

    def update_order_status(self, order_id):
        """Update order status to "pending" (success).

        params:
            order (SaleFlatOrder| str): order
            payment_success (bool): boolean, indicating sucess from GW

        """
        if type(order_id) is core_models.SalesFlatOrder:
            sale_order = order_id
        else:
            sale_order = core_models.SalesFlatOrder.objects.filter(
                increment_id=order_id)

            if not sale_order:
                raise core_exceptions.OrderNotFound()

            sale_order = sale_order.first()

        order = OrderController(None, sale_order)
        order.payment_success()

        return sale_order.status

    def verify_transaction(self, order_id, vendor_id):
        """Claim the transaction in the payment gateway.

        If claimed successfully update the status on our end.
        param:
            order_id (str) increment_id
            vendor_id (str) vendor specific Id

        """
        # Claim vendor side
        status = self.claim_payment(order_id, vendor_id)
        if status:
            # Claim on magento side
            self.update_order_status(order_id)
        else:
            tasks.send_sms.delay(order_id, 'payment_pending')


        return status

