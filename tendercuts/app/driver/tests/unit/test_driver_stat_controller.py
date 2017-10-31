"""Test cases for controller."""

import pytest
import time

from app.driver.lib.driver_stat_controller import DriverStatController
from app.driver.models import DriverOrder, DriverStat

@pytest.mark.django_db
class TestDriverStatController:
    """Test cases"""

    def test_generate_stat(self, mock_user, generate_mock_order):
        """Increase the complleted order for driver

        Asserts:
            
            Check whether the completed order is added or not.

        """

        DriverOrder.objects.create(driver_id=mock_user.customer.entity_id, increment_id=generate_mock_order.increment_id)

        stat_controller = DriverStatController()
        orders = stat_controller.generate_stat(generate_mock_order.increment_id, "complete")

        assert orders == 1
        
        DriverOrder.objects.create(driver_id=mock_user.customer.entity_id, increment_id=generate_mock_order.increment_id)

        orders = stat_controller.generate_stat(generate_mock_order.increment_id, "complete")

        assert orders == 2
        