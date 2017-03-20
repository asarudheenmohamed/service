import json
import requests

from .. import models
from app.core import models as core_models

class DriverController(object):
    """docstring for DriverController"""
    def __init__(self, driver):
        super(DriverController, self).__init__()
        self.driver = driver

    def _get_orders(self, status):
        queryset = core_models.SalesFlatOrder.objects \
            .filter(driver=self.driver) \
            .filter(status=status)
            # .filter(updated_at=str(datetime.datetime.today()))

        return queryset

    def get_completed_orders(self):
        return self._get_orders("complete")

    def get_active_orders(self):
        return self._get_orders("out_delivery")
