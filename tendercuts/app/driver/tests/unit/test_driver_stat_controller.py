"""Test cases for controller."""

import pytest
import time

from app.driver.lib.driver_stat_controller import DriverStatController
from app.driver.models import DriverOrder, DriverStat
from app.driver.lib.driver_controller import DriverController


@pytest.mark.django_db
class TestDriverStatController:
    """Test cases"""

    def test_generate_stat(self, mock_driver, generate_mock_order):
        """Increase the complleted order for driver

        Asserts:

            Check whether the completed order is added or not.

        """

        DriverOrder.objects.create(
            driver_id=mock_driver.entity_id,
            increment_id=generate_mock_order.increment_id)

        stat_controller = DriverStatController(
            generate_mock_order.increment_id)
        orders = stat_controller.generate_stat(
            generate_mock_order.increment_id, "complete")

        assert orders == 1

        DriverOrder.objects.create(
            driver_id=mock_driver.entity_id,
            increment_id=generate_mock_order.increment_id)

        orders = stat_controller.generate_stat(
            generate_mock_order.increment_id, "complete")

        assert orders == 2

    def test_driver_order_stat(self, mock_driver):
        """Increase the complleted order for driver

        Asserts:

            Check whether the completed order is added or not.

        """

        DriverStat.objects.create(
            driver_id=mock_driver.entity_id,
            no_of_orders=1)
        controller = DriverController(mock_driver.entity_id)
        obj = controller.driver_stat_orders()

        assert obj[0].no_of_orders == 1
