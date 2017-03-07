from app.tcuts import models as base_models
from .. import models
import requests
import json

class DriverController(object):
    """docstring for DriverController"""
    def __init__(self, driver):
        super(DriverController, self).__init__()
        self.driver = driver

    def _get_orders(self, status):
        queryset = base_models.SalesFlatOrder.objects \
            .filter(driver=self.driver) \
            .filter(status=status)
            # .filter(updated_at=str(datetime.datetime.today()))

        return queryset

    def get_completed_orders(self):
        return self._get_orders("complete")

    def get_active_orders(self):
        return self._get_orders("out_delivery")
