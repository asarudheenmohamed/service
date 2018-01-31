"""Test cases for Low Stock Notify customer controller."""
import datetime

import pytest

from django.utils import timezone

from app.core.models.inventory import *
from app.inventory.lib.low_stock_notification_controller import \
    LowStockNotificationController


@pytest.mark.django_db
class TestLowStockNotifyController:
    """To check Low Stock Notify Controller."""

    def test_get_low_stocks(self):
        """To check products are filered or not.

        Asserts:

            Check whether our own created product is filtered or not.

        """
        product_id = 221
        store_id = 1
        qty = 4
        status = False

        inv = Graminventory.objects.filter(
            date=datetime.date.today(),
            product_id=product_id,
            store_id=store_id,
            qty__lte=4)

        if not inv:
            obj = Graminventory.objects.create(
                product_id=product_id,
                store_id=store_id,
                qty=qty,
                expiringtoday=qty,
                forecastqty=qty,
                date=timezone.now())

        controller = LowStockNotificationController()
        low_stocks = controller.get_low_stocks()

        #  To check whether created product is filtered or not
        for product in low_stocks[store_id]:
            if product['product_id'] == product_id and product['qty'] == qty:
                status = True

        assert status == True
