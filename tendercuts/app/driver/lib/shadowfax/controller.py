from ..driver_controller import DriverController
from .request import ShadowFaxRequest
from .response import *
from ... import models as models

class ShadowFaxDriverController(DriverController):

    def __init__(self):
        self.driver = self._get_shadowfax()

    def _get_shadowfax(self):
        driver = models.DriverManagement.objects.filter(phone=9999999999)
        return driver[0]


    def push_orders(self):
        orders = self.get_active_orders()

        responses = []
        for order in orders:
            queryset = models.ShadowFaxUpdates.objects.filter(
                    client_order_id=order.increment_id)

            # we have already pushed to shadowfax don't redo it
            if len(queryset) > 0:
                continue

            responses.append(ShadowFaxRequest(order).create_order())

        return responses

    def update_order(self, data):
        try:
            response = ShadowFaxDriverCallbackResponse(data)
            response.to_model().save()
        except Exception as e:
            raise ValueError(str(e))

        return response








