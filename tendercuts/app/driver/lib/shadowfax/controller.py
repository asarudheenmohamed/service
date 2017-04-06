from ..driver_controller import DriverController
from .request import ShadowFaxRequest
from .response import *
from ... import models as models
import logging

class ShadowFaxDriverController(DriverController):

    def __init__(self ,log=None):
        self.driver = self._get_shadowfax()
        self.log = log or logging.getLogger()

    def _get_shadowfax(self):
        driver = models.DriverManagement.objects.filter(phone=9999999999)
        return driver[0]


    def push_orders(self):
        orders = self.get_active_orders()
        self.log.info("Got {} orders".format(len(orders)))


        responses = []
        for order in orders:
            self.log.info("Pushing orderid: {} for value of {}".format(
                order.increment_id, order.grand_total))
            queryset = models.ShadowFaxUpdates.objects.filter(
                    client_order_id=order.increment_id)

            # we have already pushed to shadowfax don't redo it
            if len(queryset) > 0:
                continue

            try:
                responses.append(ShadowFaxRequest(order, self.log).create_order())
            except Exception as e:
                self.log.exception(str(e))
                raise e


        return responses

    def update_order(self, data):
        try:
            response = ShadowFaxDriverCallbackResponse(data)
            print (response)
            response.to_model().save()
        except Exception as e:
            raise ValueError(str(e))

        return response








