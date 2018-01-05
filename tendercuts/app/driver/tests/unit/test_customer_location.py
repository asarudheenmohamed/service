
import time

import pytest

from app.driver.lib.customer_location import CustomerLocationController

from app.core.models.entity import EavAttribute
from app.core.models.customer import address

from app.driver import tasks


@pytest.mark.django_db
class TestCustomerLocationController:
    """Test cases for Customer location controller."""

    def test_update_customer_location(self, mock_driver, generate_mock_order):
        """Test the customer location updation.

        Asserts:
            Checks the  mock order customer location

        """
        # customer_location_obj = tasks.customer_current_location.delay(
        #     generate_mock_order.customer_id, 33333, 44444)
        customer_location_obj = CustomerLocationController().update_customer_location(
            generate_mock_order.customer_id, 1111, 222222)

        assert customer_location_obj.value == 222222
