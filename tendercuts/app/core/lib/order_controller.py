from .magento import Connector
import logging

class OrderController(object):
    """docstring for OrderController"""
    def __init__(self, magento_conn, order):
        super(OrderController, self).__init__()
        self.order = order
        self.mage = magento_conn

    def complete(self):
        response_data = self.mage.api.tendercuts_apis.completeOrders(
                [{"increment_id": self.order.increment_id}])

        return response_data

    def cancel(self):
        logging.debug("Cancelling {}".format(
                self.order.increment_id))

        status = self.mage.api.sales_order.cancel(
                    self.order.increment_id)

        if status:
            logging.info("Cancelled {}".format(self.order.increment_id))
        else:
            logging.info("Unable to Cancel {}".format(self.order.increment_id))

        return status


