"""Test cases for Low Stock Notify customer controller."""
import datetime

import pytest

from django.utils import timezone

from app.core.models.inventory import *
from app.inventory.lib.low_stock_notification_controller import \
    LowStockNotificationController
from app.inventory import tasks


@pytest.mark.django_db
class TestLowStockNotifyController:
    """To check Low Stock Notify Controller."""

    def verify_inventory(self, product_id, store_id, qty):
        """To update the inventory.

        Asserts:
            Check whether inventory is created or not.

        """
        #  To get or create inventory for check
        Graminventory.objects.update_or_create(
            date=format(datetime.datetime.today(), "%Y-%m-%d"),
            product_id=product_id,
            store_id=store_id,
            defaults={
                'qty': qty,
            }
        )


    def test_get_low_stocks(self):
        """To check products are filered or not.

        Asserts:
            Check whether our own created product is filtered or not.

        """
        product_id = 193
        store_id = 4
        qty = 2
        status = False

        self.verify_inventory(product_id, store_id, qty)
        controller = LowStockNotificationController()
        low_stocks = controller.get_low_stocks()

        #  To check whether created product is filtered or not
        for product in low_stocks[store_id]:
            if product['product_id'] == product_id:
                status = True

        assert status == True

    def _test_low_stock_notification(self):
        """To check whether store groups are receives low stock messages or not.

        Asserts:
            Checks low task messages are sends.

        """
        product_id = 221
        store_id = 4
        qty = 4

        self.verify_inventory(product_id, store_id, qty)
        response = tasks.low_stock_notification.apply()
        status = response.get()

        assert status['status'] == True
