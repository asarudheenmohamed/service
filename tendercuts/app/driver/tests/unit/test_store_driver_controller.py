"""Test cases for store driver controller."""
import pytest
from app.driver.lib.driver_controller import DriverController
from app.driver.lib.store_order_controller import StoreOrderController


@pytest.mark.django_db
class TestStoreDriverController:
    """Test cases for Store Driver controller."""

    def test_get_store_driver_order(self, mock_driver, generate_mock_order):
        """Test store driver order objects.

        Asserts:
            1. Checks driver order object increment id is equal to mock order increment id.
            2. Checks mock driver email id is equl to the response driver order
            object email id.

        """
        # assign order for the mock driver
        controller = DriverController(mock_driver.entity_id)
        driver_order = controller.assign_order(
            generate_mock_order.increment_id,
            generate_mock_order.store_id,
            12.965365,
            80.246106)

        assert driver_order.increment_id == generate_mock_order.increment_id

        controller = StoreOrderController()
        driver_order = controller.get_store_driver_order(
            generate_mock_order.store_id)

        assert generate_mock_order.increment_id in driver_order['driver_objects'][0][
            'orders']
        assert driver_order['driver_objects'][0][
            'email'] == mock_driver.customer.email
