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
            self, mock_driver, generate_mock_order, delivery_type, status):
        """Test to order pending time lapse.
        Asserts:
            Check whether the order details are fetched or not.
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

            order_data = order_controller.update_order_status_time()

        obj = OrderTimeElapsed.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert obj.increment_id == generate_mock_order.increment_id

    @pytest.mark.parametrize("delivery_type", [(1), (2)])
    def test_update_order_elapsed(
            self, mock_driver, generate_mock_order, delivery_type):
        """Test to order pending time lapse.
        Asserts:
            Check whether the order details are fetched or not.
        """

        generate_mock_order.scheduled_slot = 55
        generate_mock_order.deliverytype = delivery_type
        generate_mock_order.driver_number = 1635957311
        generate_mock_order.scheduled_date = timezone.now()
        generate_mock_order.updated_at = timezone.now().replace(hour=6, minute=00)
        generate_mock_order.save()

        obj = OrderTimeElapsed.objects.create(
            increment_id=generate_mock_order.increment_id,
            pending_time=timezone.now(),
            created_at=timezone.now(),
            processing_time=timezone.now() + timezone.timedelta(minutes=15),
            deliverytype=delivery_type,
            out_delivery_time=timezone.now() + timezone.timedelta(minutes=25),
            completed_time=timezone.now() + timezone.timedelta(minutes=40))

        order_controller = OrderTimeElapsedController(
            generate_mock_order)

        order_data = order_controller._update_order_elapsed_time(obj)
        obj = OrderTimeElapsed.objects.get(
            increment_id=generate_mock_order.increment_id)

        assert obj.increment_id == generate_mock_order.increment_id
        assert obj.out_delivery_elapsed is not 1
