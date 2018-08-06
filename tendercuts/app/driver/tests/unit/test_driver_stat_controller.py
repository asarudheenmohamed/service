"""Test cases for controller."""

import time

import pytest
from django.contrib.auth.models import User

from app.driver.lib.driver_controller import DriverController
from app.driver.lib.driver_stat_controller import DriverStatController
from app.driver.models import DriverOrder, DriverStat


@pytest.mark.django_db
class TestDriverStatController:
    """Test cases"""

    def test_generate_stat(self, mock_driver, generate_mock_order):
        """Increase the complleted order for driver

        Asserts:

            Check whether the completed order is added or not.

        """
        user_obj = User.objects.get_or_create(
            username=mock_driver.dj_user_id)[0]

        DriverOrder.objects.create(
            driver_user=user_obj,
            increment_id=generate_mock_order.increment_id)

        stat_controller = DriverStatController(
            generate_mock_order.increment_id)
        orders = stat_controller.generate_stat(
            generate_mock_order.increment_id, "complete")

        assert orders == 1

    def test_driver_order_stat(self, mock_driver):
        """Increase the complleted order for driver

        Asserts:

            Check whether the completed order is added or not.

        """
        user_obj = User.objects.get_or_create(
            username=mock_driver.dj_user_id)[0]
        DriverStat.objects.create(
            driver_user=user_obj,
            no_of_orders=1)
        controller = DriverController(user_obj)
        obj = controller.driver_stat_orders()

        assert obj[0].no_of_orders == 1
