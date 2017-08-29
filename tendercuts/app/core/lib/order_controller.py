"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging
from .magento import Connector
from app.core.models.sales_order import SalesFlatOrderGrid


class OrderController(object):
    """
    Update order status
    """

    def __init__(self, magento_conn, order):
        super(OrderController, self).__init__()
        self.order = order
        self.mage = magento_conn

    def processing(self):
        """The order status pending to processing state."""
        invoice_id = self.mage.api.sales_order_invoice.create(
            {'invoiceIncrementId ': self.order.increment_id})
        self.mage.api.sales_order_invoice.capture(
            {'invoiceIncrementId ': invoice_id})

    def out_delivery(self):
        """The order status processing to out for delivery."""
        self.order.status = "out_delivery"
        self.order.save()
        obj = SalesFlatOrderGrid.objects.get(
            increment_id=self.order.increment_id)
        obj.status = "out_delivery"
        obj.save()
        # a = self.mage.api.sales_order_shipment.info(self.order.increment_id)

    def complete(self):
        """
        Using the SOAP API here, as we need to triggers observers in magento for
        reward and credit.
        """
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
        """If payment in successful, update status.

        1. Update status as "pending" for express
        2. Update status as sch_order for scheduled
        3. Update as pending for split order
        4. Grid also needs to be updated.
        """
        # express delivery
        if self.order.deliverytype == 1:
            self.order.status = "pending"
            self.order.grid.status = "pending"
        # sch
        elif self.order.deliverytype == 2:
            self.order.status = "scheduled_order"
            self.order.grid.status = "scheduled_order"
        # split
        else:
            self.order.status = "pending"
            self.order.grid.status = "pending"

        self.order.save()
        self.order.grid.save()

    def update_payment_status(self):
        """Update the payment_received flag.

        Ideally this should be merged with payment_sucess eventually
        """
        self.order.payment_received = 1
        self.order.save()
