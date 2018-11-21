from .base_action import BaseAction
from app.core.models import SalesFlatOrder


class OrderStatusAction(BaseAction):
    def __init__(self, data):
        super(OrderStatusAction, self).__init__(data)

    @property
    def orderId(self):
        return self.params['orderId']['orderId']

    def execute(self):
        """order id

        :return: (str)
        """
        order = SalesFlatOrder.objects.filter(
            increment_id=int(self.orderId)).first()
            
        response = "Order #{} is current in {} stage at {}. \n".format(
                int(self.orderId), order.status, order.store_id)

        if order.status == 'out_delivery':
            response += "The order is carried by {}({})".format(
                order.driver_name,
                order.driver_number
            )
        
        if order.status == 'complete':
            response += "The order was carried by {}({})".format(
                order.driver_name,
                order.driver_number
            )

        return response
