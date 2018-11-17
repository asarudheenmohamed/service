from .base_action import BaseAction
from app.core.models import SalesFlatOrder
from app.core.lib.order_controller import OrderController
import app.core.lib.magento as mage


class CancelOrderAction(BaseAction):
    def __init__(self, data):
        super(CancelOrderAction, self).__init__(data)

    @property
    def orderId(self):
        return self.params['orderId']['orderId']

    def execute(self):
        """order id

        :return: (str)
        """
        conn = mage.Connector()
        order = SalesFlatOrder.objects.filter(
            increment_id=int(self.orderId))
        controller = OrderController(conn, order)
        try:
            controller.cancel()
            response = "Order #{} has been cancelled".format(
                int(self.orderId))
        except Exception:
            response = "Unable to cancel Order #{}, please check with tech support".format(
                int(self.orderId))

        return response
