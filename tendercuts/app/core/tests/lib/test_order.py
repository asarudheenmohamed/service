"""
Test cases for testing orders contrller
"""

import pytest
from app.core.models.sales_order import *
from app.core.lib.order_controller import OrderController


@pytest.mark.django_db
class TestOrderController:
    """
    Companion for Order Controller
    """

    def test_order_express(self):
        """
        Asserts:
         Instance is valid
        """
        # mock the order
        order = SalesFlatOrder.objects.filter(entity_id=1)[0]
        order.status = "pending_payment"
        order.grid.status = "pending_payment"
        order.order_now = 1
        order.save()
        order.grid.save()

        # no need mage controller
        ord_ctrl = OrderController(None, order)
        ord_ctrl.payment_success()

        order = SalesFlatOrder.objects.filter(entity_id=1)[0]
        assert order.status == "pending"
        assert order.grid.status == "pending"

    def test_order_scheduled(self):
        """
        Asserts:
         Instance is valid
        """
        # mock the order
        order = SalesFlatOrder.objects.filter(entity_id=1)[0]
        order.status = "pending_payment"
        order.grid.status = "pending_payment"
        order.order_now = 0
        order.save()
        order.grid.save()

        # no need mage controller
        ord_ctrl = OrderController(None, order)
        ord_ctrl.payment_success()

        order = SalesFlatOrder.objects.filter(entity_id=1)[0]
        assert order.status == "scheduled_order"
        assert order.grid.status == "scheduled_order"
