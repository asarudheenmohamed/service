from app.core.models import SalesFlatOrder
from .base_action import BaseAction


class OrderRefund(BaseAction):
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
        return self.params['refundMode']

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

        return "Done"
