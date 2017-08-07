"""Test cases for controller."""

import pytest
import time

from app.driver.lib.driver_controller import DriverController
from app.driver.models import DriverOrder


@pytest.mark.django_db
class TestDriverController:
    """Test cases"""

    def test_driver_assignment(self, mock_user, generate_mock_order):
        """Assign driver test case.

        Asserts:
            1. If the driver is assigned

        """
        controller = DriverController(mock_user)
        driver_order = controller.assign_order(generate_mock_order)

        assert driver_order.increment_id == generate_mock_order.increment_id

    @pytest.mark.parametrize('status', ['out_delivery', 'complete'])
    def test_fetch_active_order(self, mock_user, generate_mock_order, status):
        """Fetch all the active orders.

        Asserts:
            1. If the assigned order is fetched.

        """
        # mock status
        generate_mock_order.status = status
        generate_mock_order.save()

        # mock driver
        DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_id=mock_user.customer.entity_id).save()

        controller = DriverController(mock_user)
        orders = controller.fetch_orders(status)

        assert len(orders) == 1
    
    def test_complete_order(self, mock_user, generate_mock_order):
        """complete the order.

        Asserts:
            1. If the assigned order is completed.

        """
        # mock status
        generate_mock_order.status = 'out_delivery'
        generate_mock_order.save()

        # mock driver
        DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_id=mock_user.customer.entity_id).save()

        controller = DriverController(mock_user)
        orders = controller.complete_order(generate_mock_order.increment_id)
