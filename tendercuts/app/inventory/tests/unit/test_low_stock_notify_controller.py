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

    def test_inventory_update(self, product_id, store_id, qty):
        """To update the inventory.

        Asserts:
            Check whether inventory is created or not.

        """
        #  To get or create inventory for check
        obj = Graminventory.objects.get_or_create(
            product_id=product_id,
            store_id=store_id,
            qty=qty,
            expiringtoday=qty,
            forecastqty=qty,
            date=timezone.now())

        assert obj is not []

    def test_get_low_stocks(self):
        """To check products are filered or not.

        Asserts:
            Check whether our own created product is filtered or not.

        """
        product_id = 221
        store_id = 5
        qty = 4
        status = False

        self.test_inventory_update(product_id, store_id, qty)
        controller = LowStockNotificationController()
        low_stocks = controller.get_low_stocks()

        #  To check whether created product is filtered or not
        for product in low_stocks[store_id]:
            if product['product_id'] == product_id and product['qty'] == qty:
                status = True

        assert status == True

    def test_low_stock_notification(self):
        """To check whether store groups are receives low stock messages or not.

        Asserts:
            Checks low task messages are sends.

        """
        product_id = 221
        store_id = 7
        qty = 4

        self.test_inventory_update(product_id, store_id, qty)
        response = tasks.low_stock_notification.apply()
        status = response.get()

        assert status['status'] == True
