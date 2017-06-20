"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging
from .magento import Connector


class OrderController(object):
    """
    Update order status
    """

    def __init__(self, magento_conn, order):
        super(OrderController, self).__init__()
        self.order = order
        self.mage = magento_conn

    def complete(self):
        """
        Using the SOAP API here, as we need to triggers observers in magento for
        reward and credit.
        """
        invoice_id = self.mage.api.sales_order_invoice.create(
            {'orderIncrementId': self.order.increment_id})
        self.mage.api.sales_order_invoice.capture(
            {'invoiceIncrementId ': invoice_id})
        response_data = self.mage.api.sales_order_shipment.create(
            {'orderIncrementId': self.order.increment_id})

        return response_data

    def cancel(self):
        """
        Triggring soap api here to enable any Mage observer
        """
        logging.debug("Cancelling {}".format(self.order.increment_id))

        status = self.mage.api.sales_order.cancel(
            self.order.increment_id)

        if status:
            logging.info("Cancelled {}".format(self.order.increment_id))
        else:
            logging.info("Unable to Cancel {}".format(self.order.increment_id))

        return status

    def payment_success(self):
        """
        If payment in successful

        1. Update status as "pending" for express
        2. Update status as sch_order for scheduled
        2. Grid also needs to be updated.
        """
        # express delivery
        if self.order.order_now == 1:
            self.order.status = "pending"
            self.order.grid.status = "pending"
        elif self.order.order_now == 0:
            self.order.status = "scheduled_order"
            self.order.grid.status = "scheduled_order"

        self.order.save()
        self.order.grid.save()
