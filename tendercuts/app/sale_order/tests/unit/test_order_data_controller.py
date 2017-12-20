"""Test cases for order data controller."""

import pytest
import time

from app.sale_order.lib import OrderDataController


@pytest.mark.django_db
class TestOrderDataController:
    """Test cases"""

    def test_order_data(self, mock_user, generate_mock_order):
        """To get the required order details

        Asserts:

            Check whether the order details are fetched or not.

        """
        order_controller = OrderDataController(
            generate_mock_order.increment_id)
        order_data = order_controller.order_details(
            generate_mock_order.increment_id)

        assert generate_mock_order.increment_id == order_data[0]['increment_id']
