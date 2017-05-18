"""
Every payment GW should implement this class
"""

from app.core.lib.order_controller import OrderController
from app.core import models as core_models
from app.core.lib import exceptions as core_exceptions

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
        """
        Payment mehtod name in magento
        """
        pass

    @abc.abstractmethod
    def check_payment_status(self, order_id, vendor_id):
        """
        Check the status of the order
        param:
            order_id (str) increment_id
            vendor_id (str) vendor specific Id
        """
        pass

    def update_order_status(self, order_id):
        """
        Updates order

        params:
            order (SaleFlatOrder): order
            payment_success (bool): boolean, indicating sucess from GW
        """
        sale_order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)

        if not sale_order:
            raise core_exceptions.OrderNotFound()

        order = OrderController(None, sale_order[0])
        order.payment_success()

        return sale_order[0].status

    def verify_transaction(self, order_id, vendor_id):
        """
        Check the status of the order and update the magento state
        param:
            order_id (str) increment_id
            vendor_id (str) vendor specific Id
        """
        status = self.check_payment_status(order_id, vendor_id)
        if status:
            self.update_order_status(order_id)

        return status
