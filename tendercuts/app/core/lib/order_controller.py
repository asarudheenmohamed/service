"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging

from django.utils import timezone

from app.core.models.sales_order import (SalesFlatOrderGrid,
                                         SalesFlatOrderStatusHistory)

from .magento import Connector

logger = logging.getLogger(__name__)


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
        response_data = self.mage.api.tendercuts_order_apis.updateOutForDelivery(
            [{'increment_id': self.order.increment_id}])
        logger.info(
            'This order:{} was changed to out for delivery'.format(
                self.order.increment_id))

        response_data

    def complete(self):
        """
        Using the megento custom API here, as we need to triggers observers in magento for
        reward and credit.

        """
        response_data = self.mage.api.tendercuts_order_apis.completeOrders(
            [{'increment_id': self.order.increment_id}])

        return response_data

    def cancel(self):
        """
        Triggring soap api here to enable any Mage observer
        """
        logger.debug("Cancelling {}".format(self.order.increment_id))

        status = self.mage.api.sales_order.cancel(
            self.order.increment_id)

        if status:
            logger.info("Cancelled {}".format(self.order.increment_id))
        else:
            logger.info("Unable to Cancel {}".format(self.order.increment_id))

        return status

    def payment_success(self, is_comment=None):
        """If payment in successful, update status.

        1. Update status as "pending" for express
        2. Update status as sch_order for scheduled
        3. Update as pending for split order
        4. Grid also needs to be updated.
        """
        # express delivery
        if self.order.deliverytype == 1:
            status = "pending"
        # sch
        elif self.order.deliverytype == 2:
            status = "scheduled_order"
        # split
        else:
            status = "pending"

        self.order.status = status
        self.order.save()

        if getattr(self.order, "grid", None):
            self.order.grid.status = "pending"
            self.order.grid.save()

        if is_comment:
            # update order status history
            SalesFlatOrderStatusHistory.objects.create(
                parent=self.order,
                status=status,
                created_at=timezone.now(),
                comment=is_comment,
                is_customer_notified=1,
                is_visible_on_front=1,
                entity_name='order')

    def update_payment_status(self):
        """Update the payment_received flag.

        Ideally this should be merged with payment_sucess eventually
        DEPRECATED
        """
        self.order.payment_received = 1
        self.order.save()
