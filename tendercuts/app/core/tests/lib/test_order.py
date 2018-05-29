"""Test cases for testing orders contrller."""

import pytest
from app.core.models.sales_order import SalesFlatOrder, SalesFlatOrderStatusHistory
from app.core.lib.order_controller import OrderController


@pytest.mark.django_db
class TestOrderController:
    """
    Companion for Order Controller
    """

    @pytest.mark.parametrize("status,delivery_type,comment", [
        ("pending_payment", 1, "Payment verify fron juspay"),
        ("pending_payment", 2, None)])
    def test_order_payment_success(
            self, status, delivery_type, comment):
        """
        Asserts:
         Checks the mock order status
        """
        # mock the order

        generate_mock_order = SalesFlatOrder.objects.filter(
            deliverytype=delivery_type).last()
        generate_mock_order.scheduled_slot = 52
        generate_mock_order.status = status
        generate_mock_order.save()

        ord_ctrl = OrderController(None, generate_mock_order)
        ord_ctrl.payment_success(is_comment=comment)

        order = SalesFlatOrder.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert order.status in ["pending", "scheduled_order"]
        assert order.grid.status in ["pending", "scheduled_order"]

        response = SalesFlatOrderStatusHistory.objects.filter(
            parent__increment_id=order.increment_id).last()

        assert response.comment in ["Payment verify fron juspay", None]
