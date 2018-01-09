"""Test cases for controller."""

import time

import pytest

import app.core.lib.magento as mage
from app.core.lib.order_controller import OrderController
from app.driver.models import DriverOrder
from app.driver.lib.driver_controller import DriverController


@pytest.mark.django_db
class TestDriverController:
    """Test cases for Driver controller."""

    def test_driver_assignment(self, mock_driver, generate_mock_order):
        """Assign driver test case.

        Asserts:
            1. If the driver is assigned

        """
        controller = DriverController(mock_driver.entity_id)
        driver_order = controller.assign_order(
            generate_mock_order.increment_id,
            generate_mock_order.store_id,
            12.965365,
            80.246106)

        assert driver_order.increment_id == generate_mock_order.increment_id

    @pytest.mark.parametrize('status', ['out_delivery', 'complete'])
    def test_fetch_active_order(
            self, mock_driver, generate_mock_order, status):
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
            driver_id=mock_driver.entity_id).save()

        controller = DriverController(mock_driver.entity_id)
        orders = controller.fetch_orders(status)

        assert len(orders) == 1

    def test_fetch_related_order(
            self, auth_rest, mock_driver, generate_mock_order):
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
        # controller.processing()
        generate_mock_order.status = 'processing'
        generate_mock_order.save()
        increment_id = str(generate_mock_order.increment_id)
        controller = DriverController(mock_driver.entity_id)
        orders = controller.fetch_related_orders(
            increment_id[4:], generate_mock_order.store_id)

        assert (orders) is not None
        assert orders[0].increment_id == generate_mock_order.increment_id

    def test_complete_order(self, mock_driver, generate_mock_order):
        """Complete the order.

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
            driver_id=mock_driver.entity_id).save()
        controller = DriverController(mock_driver.entity_id)
        orders = controller.complete_order(generate_mock_order.increment_id, 12.965365,
                                           80.246106)
        print orders

    def test_order_positions(self, mock_driver, generate_mock_order):
        """Test Drive Position updated and driver order events update.

        Asserts:
            Check response latitude and longitude.
            Check response increment id is equal to mock order id

        """
        # mock driver
        obj = DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_id=mock_driver.entity_id)

        controller = DriverController(mock_driver.entity_id)
        # test record position
        response = controller.record_position(
            12.965365,
            80.246106)

        assert response.latitude == 12.965365
        assert response.longitude == 80.246106

        # test order events
        response = controller._record_events(obj,
                                             response, 'out_delivery')

        assert response.driver.increment_id == generate_mock_order.increment_id

    def test_driver_delay_sms(self, mock_driver, generate_mock_order):
        """Test Customer receives the SMS.

        Asserts:
            Check status

        """
        controller = DriverController(mock_driver.entity_id)
        customer = controller.driver_delay_sms(
            generate_mock_order.increment_id)

        assert customer is True
