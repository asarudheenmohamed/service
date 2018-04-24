"""Test cases for order data controller."""

import time
from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from app.core.models import SalesFlatOrder, SalesFlatOrderItem
from app.sale_order.lib.order_time_lapse_controller import \
    OrderTimelapseController
from app.sale_order.models import OrderTimelapse


@pytest.mark.django_db
class TestOrderDataController:
    """Test cases"""

    @pytest.mark.parametrize("delivery_type", [
        (None),  # fetch express
        (2),  # fetch schedule,
    ])
    def test_pending_time_calculation(

            self, generate_mock_order, delivery_type):
        """Test to order pending time lapse.
        Asserts:
            Check whether the order details are fetched or not.
        """

        generate_mock_order.slot = 52
        generate_mock_order.delivery_type = delivery_type
        generate_mock_order.driver_number = 1635957311
        generate_mock_order.updated_at = timezone.now().replace(hour=6, minute=00)
        generate_mock_order.save()

        order_controller = OrderTimelapseController(
            generate_mock_order)
        order_data = order_controller.compute_order_pending_time_lapse()

        obj = OrderTimelapse.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert obj.increment_id == generate_mock_order.increment_id

    @pytest.mark.parametrize("delivery_type,lapse", [
        (None, 60),  # fetch express
        (2, -60),  # fetch schedule,
    ])
    def test_processing_time_calculation(
            self, generate_mock_order, delivery_type, lapse):
        """Test to order processing time lapse.

        Asserts:

            Check whether the order processing lapse.

        """

        generate_mock_order.slot = 52
        generate_mock_order.delivery_type = delivery_type
        generate_mock_order.scheduled_date = timezone.now()
        generate_mock_order.updated_at = timezone.now().replace(hour=6, minute=00)
        generate_mock_order.save()

        obj = OrderTimelapse.objects.get_or_create(
            increment_id=generate_mock_order.increment_id, processing_time=generate_mock_order.updated_at + timedelta(hours=-1))

        order_controller = OrderTimelapseController(
            generate_mock_order)

        order_data = order_controller.compute_order_processing_time_lapse()

        obj = OrderTimelapse.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert obj.processing_lapse == lapse

    @pytest.mark.parametrize("delivery_type,lapse", [
        (None, 60),  # fetch express
        (2, -60),  # fetch schedule,
    ])
    def test_out_delivery_time_calculation(
            self, generate_mock_order, delivery_type, lapse):
        """Test to order out delivery time lapse.

        Asserts:

            Check whether the order out delivery lapse.

        """

        generate_mock_order.slot = 52
        generate_mock_order.delivery_type = delivery_type
        generate_mock_order.scheduled_date = timezone.now()
        generate_mock_order.updated_at = timezone.now().replace(hour=6, minute=00)
        generate_mock_order.save()

        obj = OrderTimelapse.objects.get_or_create(
            increment_id=generate_mock_order.increment_id, out_delivery_time=generate_mock_order.updated_at + timedelta(hours=-1))

        order_controller = OrderTimelapseController(
            generate_mock_order)

        order_data = order_controller.compute_order_out_delivery_time_lapse()

        obj = OrderTimelapse.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert obj.out_delivery_lapse == lapse
