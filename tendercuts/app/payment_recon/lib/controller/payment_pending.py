from ... import models as models
from datetime import date, timedelta
from ..gateway import Payu
from django.utils import timezone
from app.core.lib.order_controller import OrderController
from app.core.lib.magento import Connector
import logging

import dateutil.parser as dt_parser

class PaymentAutomationController():

    def __init__(self, gateway, log=None):
        self.gateway = gateway
        self.mage = Connector()
        self.log = log or logging.getLogger()

    def fetch_orders(self, threshold=60 * 15, statuses=None):
        """
        Fetches all pending orders from payu.
        """

        statuses = statuses or ("pending_payment", "payment_pending")
        start = date.today()
        start = dt_parser.parse("2017-03-23")
        end = date.today() + timedelta(days=1)
        orders = models.SalesFlatOrder.objects \
            .filter(created_at__range=(start, end),
                    status__in=statuses) \
            .prefetch_related("payment")

        self.log.info("Fetched {} payment_pending orders".format(
            len(orders)))

        # TODO MOVE IS_PAYU TO A SEP CONTROLLER!
        # Filter only payu order
        orders = [order for order in orders if order.is_payu]

        if threshold is not None:
            orders = [order for order in orders
                if order.time_elapsed().seconds > threshold]

        self.log.info("Fetched {} payment_pending orders to be queried".format(
            len(orders)))
        return orders


    def cancel_pending_orders(self, dry_run=True):
        """
        If any order is in pending payment for more than 10 mins
        cancel it
        """
        orders = self.fetch_orders(statuses=("pending_payment", "payment_pending"))
        order_map = {order.increment_id: order for order in orders}
        statuses = self.gateway.check_payment_status(orders)

        for status in statuses:

            if dry_run:
                continue

            if status.vendor_status == "success":
                # More to come here, need to move to pending
                continue

            # Save the record and cancel the order
            order = order_map[status.tpn]
            self.log.info("Cancelling {}".format(order.increment_id))
            status.save()

            try:
                order_controller = OrderController(self.mage, order)
                order_controller.cancel()
            except Exception as e:
                self.log.error(str(e))


        return statuses


    def refund_payu_cancelled_orders(self, today=None):
        """
        PAYU SPECIFIC: needs to be moved to a separate class
        """
        orders = self.fetch_orders(statuses=["closed", "canceled", "pending_payment", "payment_pending"], threshold=None)
        order_map = {order.increment_id: order for order in orders}

        if not orders:
            self.log.info("Whoo hoo no orders are in closing state")
            return []

        statuses = self.gateway.check_payment_status(orders)

        # Bulk fetch from payu
        for status in statuses:

            # If the payment has failed or something, then dont't bother!
            # as the order is already in closed state and not payment has been captured
            if status.vendor_status != "success":
                continue

            print(status.tpn)


    def detect_failed_to_capture_payments(self, today=None):
        """
        PAYU SPECIFIC: needs to be moved to a separate class
        """
        orders = self.fetch_orders(statuses=["complete", "processing", "out_delivery", "pending"], threshold=None)
        order_map = {order.increment_id: order for order in orders}

        if not orders:
            self.log.info("Whoo hoo no orders are in closing state")
            return []

        statuses = self.gateway.check_payment_status(orders)

        order_ids = []
        # Bulk fetch from payu
        for status in statuses:

            # If the payment has failed or something, then dont't bother!
            # as the order is already in closed state and not payment has been captured
            if status.vendor_status == "success":
                continue

            order_ids.append(status.tpn)

        return order_ids
