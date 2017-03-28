from ... import models as models
from datetime import date, timedelta
from ..gateway import Payu
from django.utils import timezone
from app.core.lib.order_controller import OrderController
from app.core.lib.magento import Connector
import logging

class PaymentAutomationController():

    def __init__(self, gateway):
        self.gateway = gateway
        self.mage = Connector()

    def fetch_pending_orders(self, threshold=60 * 10):
        """
        Fetches all pending orders from payu.
        """
        start = date.today()
        end = date.today() + timedelta(days=1)
        orders = models.SalesFlatOrder.objects \
            .filter(created_at__range=(start, end),
                    status__in=("pending_payment",
                                "payment_pending")) \
            .prefetch_related("payment")

        logging.info("Fetched {} payment_pending orders".format(
            len(orders)))
        # get only payu orders
        orders = [order for order in orders 
            if order.is_payu and order.time_elapsed().seconds > threshold]

        logging.info("Fetched {} payment_pending orders to be queried".format(
            len(orders)))
        return orders

    def cancel_pending_orders(self, dry_run=True):
        """
        If any order is in pending payment for more than 10 mins
        cancel it
        """
        orders = self.fetch_pending_orders()
        order_map = {order.increment_id: order for order in orders}
        statuses = self.gateway.check_payment_status(orders)

        for status in statuses:

            if dry_run:
                continue

            if status.is_payment_captured:
                # More to come here, need to move to pending
                continue

            # Save the record and cancel the order
            status.save()

            order = order_map[status.tpn]
            order_controller = OrderController(self.mage, order)
            order_controller.cancel()

        return statuses

