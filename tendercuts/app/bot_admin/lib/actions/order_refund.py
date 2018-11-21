import logging

from app.driver import tasks as driver_tasks
from app.core.models import SalesFlatOrder
from app.payment.lib.gateway.juspay.mixin import JuspayMixin
from .base_action import BaseAction
from app.core.lib.order_controller import OrderController
import app.core.lib.magento as mage

logger = logging.getLogger(__name__)


class OrderRefund(JuspayMixin, BaseAction):
    def __init__(self, data):
        super(OrderRefund, self).__init__(data)

    @property
    def orderId(self):
        return self.params['orderId']['orderId']

    @property
    def confirm(self):
        return self.params['confirmed']

    @property
    def refund_mode(self):
        """Can be either PG/WALLET"""
        return self.params['refundMode']

    def _handle_juspay_refund(self, order):
        """Triggers a refund at juspay and sends an sms to customer.

        :return the response
        """
        response = self.juspay.Orders.refund(
            unique_request_id=order.increment_id,
            order_id=order.increment_id,
            amount=order.grand_total)

        logger.info(
            "BOT: Payment refunded to the order:{} for {} with {}".format(
                order.increment_id,
                order.grand_total,
                response.__dict__
            ))

        # SMS TRIGGERING
        driver_tasks.send_sms.delay(order.increment_id, 'payment_refunded')
        logger.info(
            "BOT: Sent payment refund message to the order:{}".format(
                order.increment_id))

        response = "{} has been refunded for the order {} " \
                   "for the payment mode {}. \n".format(
            response.amount, response.refunded, response.payment_method)

        return response

    def _cancel_mage_order(self, order, response):
        """CHeck and cancel the mage order, if already in closed state then don't
        handle it."""
        if order.status in ("canceled", "closed"):
            response += "The order has alredy been closed, so not closing it."
            return response

        conn = mage.Connector()
        controller = OrderController(conn, order)
        try:
            controller.cancel()
            response += "Order #{} has been cancelled".format(
                int(self.orderId))
        except Exception:
            response += \
                "Unable to cancel Order #{}, please check with tech support." \
                "Also not the payment for this order has been refunded, " \
                "So this order needs to be closed ASAP".format(int(self.orderId))

        return response

    def execute(self):
        """order id

        :return: (str)
        """

        if self.confirm != "yes":
            return "Since you didn't give me confirmation, " \
                   "I'm not going to do anything."

        order = SalesFlatOrder.objects \
            .filter(increment_id=int(self.orderId)) \
            .prefetch_related('payment') \
            .first()

        if order.status == "complete":
            return "The order is already complete." \
                   "I can't do much here, you better contact tech support."

        mode = order.payment.first().method

        if mode != "juspay":
            return "Currently I only know how to refund juspay orders, " \
                   "this order is has a payment mode: {}".format(mode)

        if self.refund_mode == "PG":
            response = self._handle_juspay_refund(order)
            response = self._cancel_mage_order(order, response)
            return response


        return "TODO add wallet handling"
