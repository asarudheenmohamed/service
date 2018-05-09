"""Test cases for order data controller."""

import time
from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from app.core.models import SalesFlatOrder, SalesFlatOrderItem
from app.sale_order.lib.order_time_elapsed_controller import OrderTimeElapsedController
from app.sale_order.model import OrderTimeElapsed


@pytest.mark.django_db
class TestOrderDataController:
    """Test cases"""

    @pytest.mark.parametrize("delivery_type,status", [
        (1, ("pending", "processing", "out_delivery", "complete"))])
    def test_update_order_status_time(
            self, mock_driver, delivery_type, status):
        """Test to order elapsed time lapse.
        Asserts:
            Checks the order elapsed object increment id is mock order increment_id.
        """
        for state in status:
            generate_mock_order.status = state
            generate_mock_order.scheduled_slot = 52
            generate_mock_order.deliverytype = delivery_type
            generate_mock_order.driver_number = mock_driver._flat[
                'mobilenumber']
            generate_mock_order.updated_at = timezone.now().replace(hour=6, minute=00)
            generate_mock_order.save()

            order_controller = OrderTimeElapsedController(
                generate_mock_order)

            order_data = order_controller.update_order_status_time(state)

        obj = OrderTimeElapsed.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert obj.increment_id == generate_mock_order.increment_id
