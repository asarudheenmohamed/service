"""Test cases for controller."""

import time

import mock
import pytest

from django.contrib.auth.models import User
import app.core.lib.magento as mage
from app.core.lib.order_controller import OrderController
from app.core.lib.user_controller import CustomerSearchController
from app.driver.lib.driver_controller import DriverController
import mock

from app.driver.lib.trip_controller import TripController
from app.driver.models import DriverOrder


@pytest.mark.django_db
class TestDriverController:
    """Test cases for Driver controller."""

    def test_driver_assignment(
            self, mock_driver, django_user, generate_mock_order):
        """Assign driver test case.

        Asserts:
            1. If the driver is assigned

        """
        print mock_driver.entity_id
        controller = DriverController(django_user)
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

        user = User.objects.get_or_create(username=mock_driver.dj_user_id)[0]
        DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_user=user)
        controller = DriverController(user)
        orders = controller.fetch_orders(status)
        assert len(orders) == 1

    def test_fetch_related_order(
            self, auth_rest, mock_driver, django_user, generate_mock_order):
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

        generate_mock_order.status = 'processing'
        generate_mock_order.save()
        increment_id = str(generate_mock_order.increment_id)
        controller = DriverController(django_user)
        orders = controller.fetch_related_orders(
            increment_id[4:], generate_mock_order.store_id)
        assert (orders) is not None
        assert orders[0].increment_id == generate_mock_order.increment_id

    def test_complete_order(
            self, mock_driver, generate_mock_order):
        """Complete the order.

        Asserts:
            1. If the assigned order is completed.

        """
        # mock status
        conn = mage.Connector()
        controller = OrderController(conn, generate_mock_order)
        controller.out_delivery()

        # mock driver
        user = User.objects.get_or_create(username=mock_driver.dj_user_id)[0]
        DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_user=user)
        controller = DriverController(user)

        with mock.patch.object(TripController, 'check_and_complete_trip',
                               mock.Mock(return_value=None)):

            orders = controller.complete_order(generate_mock_order.increment_id, 12.965365,
                                               80.246106)
        print orders

    def test_order_positions(
            self, mock_driver, generate_mock_order):
        """Test Drive Position updated and driver order events update.

        Asserts:
            Check response latitude and longitude.
            Check response increment id is equal to mock order id

        """
        # mock driver
        user = User.objects.get_or_create(username=mock_driver.dj_user_id)[0]
        obj = DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_user=user)

        controller = DriverController(user)
        # test record position
        response = controller.record_position(
            12.965365,
            80.246106)

        assert response.latitude == 12.965365
        assert response.longitude == 80.246106

        # test order events
        response = controller._record_events(obj, response, 'out_delivery')

        assert response.driver_order.increment_id == generate_mock_order.increment_id

    def test_driver_delay_sms(
            self, mock_driver, django_user, generate_mock_order):
        """Test Customer receives the SMS.

        Asserts:
            Check status

        """
        controller = DriverController(django_user)
        customer = controller.driver_delay_sms(
            generate_mock_order.increment_id)

        assert customer is True

    def test_update_driver_details(
            self, mock_driver, generate_mock_order):
        """Test update driver details functionality.

        Asserts:
            Check mock driver details is equal to generate_mock_order assigned
            driver details

        """
        # mock driver

        driver_details = CustomerSearchController.load_cache_basic_info(
            mock_driver.entity_id)
        user = User.objects.get_or_create(username=mock_driver.dj_user_id)[0]
        controller = DriverController(user)

        response = controller.update_driver_details(
            generate_mock_order)

        assert generate_mock_order.driver_number == driver_details['phone']
        assert generate_mock_order.driver_name == driver_details['name']
