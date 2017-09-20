"""Test cases for controller."""

import time

import pytest

import app.core.lib.magento as mage
from app.core.lib.order_controller import OrderController
from app.driver.models import DriverOrder
from app.driver.lib.driver_controller import DriverController


@pytest.mark.django_db
class TestDriverController:
    """Test cases for Driver controller"""

    def test_driver_assignment(self, mock_user, generate_mock_order):
        """Assign driver test case.

        Asserts:
            1. If the driver is assigned

        """
        controller = DriverController(mock_user)
        driver_order = controller.assign_order(
            generate_mock_order.increment_id,
            generate_mock_order.store_id,
            12.965365,
            80.246106)

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

    def test_fetch_related_order(
            self, auth_rest, mock_user, generate_mock_order):
        """Generate mock order and Fetch relevent orders based on mock order id.

        Params:
            auth_rest(pytest fixture): user requests
            generate_mock_order(obj): mock order object

        Asserts:
            Check response not equal to None
            Check response increment id is equal to mock order id.

        """
        # change generate order status pending to processing
        conn = mage.Connector()
        controller = OrderController(conn, generate_mock_order)
        controller.processing()

        increment_id = str(generate_mock_order.increment_id)
        inc_id = list(increment_id)
        increment = increment_id.split(inc_id[3])

        controller = DriverController(mock_user)
        orders = controller.fetch_related_orders(
            increment[-1], generate_mock_order.store_id)

        assert (orders) is not None
        assert orders[0].increment_id == generate_mock_order.increment_id

    def test_complete_order(self, mock_user, generate_mock_order):
        """complete the order.

        Asserts:
            1. If the assigned order is completed.

        """
        # mock status
        conn = mage.Connector()
        controller = OrderController(conn, generate_mock_order)
        controller.out_delivery()

        # mock driver
        DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_id=mock_user.customer.entity_id).save()
        controller = DriverController(mock_user)
        orders = controller.complete_order(generate_mock_order.increment_id, 12.965365,
                                           80.246106)
        print orders

    def test_order_positions(self, mock_user, generate_mock_order):
        """Test Drive Position updated and driver order events update.

        Asserts:
            Check response latitude and longitude.
            Check response increment id is equal to mock order id

        """
        # mock driver
        obj = DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_id=mock_user.customer.entity_id)

        controller = DriverController(mock_user)
        # test record position
        response = controller.record_position(generate_mock_order.increment_id,
                                              12.965365,
                                              80.246106)

        assert response.latitude == 12.965365
        assert response.longitude == 80.246106

        # test order events
        response = controller.record_events(
            response, 'out_delivery')

        assert response.driver_position.driver.increment_id == generate_mock_order.increment_id
