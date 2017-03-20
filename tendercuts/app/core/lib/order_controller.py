from ..core import magento_api as magento

class OrderController(object):
    """docstring for OrderController"""
    def __init__(self, order):
        super(OrderController, self).__init__()
        self.order = order
        self.mage = magento.Connector()

    def complete_order(self):
        response_data = self.mage.api.tendercuts_apis.completeOrders(
                [{"increment_id": self.order.increment_id}])

        return response_data
