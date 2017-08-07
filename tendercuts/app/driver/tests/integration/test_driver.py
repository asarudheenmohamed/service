"""Integration tests for driver module.

Pre-requisite: The mage consumer should be running

"""

import pytest
import time

from pytest_bdd import given, when, then, scenario
from app.driver.lib.driver_controller import DriverController
from app.core.models import SalesFlatOrder


@pytest.mark.django_db
@scenario(
    'driver.feature',
    'Driver sucessfully completes the order',
)
def test_driver_order_complete():
    pass


# Reuse the mock order fixture
given(
    'A customer places an order',
    fixture='generate_mock_order')


@given('a driver is assigned to the order')
def driver_controller(mock_user, generate_mock_order):
    """Assign the order.

    params:
        mock_user (fixture) - generates a driver object
        generate_mock_order (fixture) - generates a mock order.

    """
    controller = DriverController(mock_user)
    controller.assign_order(generate_mock_order)

    return controller


@when('the driver completes the order')
def complete_order(driver_controller, generate_mock_order):
    """Complete the order.

    Asserts:
        Verify if the order is set in out_delivery stat

    params:
        driver_controller (fixture) - generates a driver object.
        generate_mock_order (fixture) - generates a mock order.

    """
    time.sleep(5)
    order = SalesFlatOrder.objects.filter(
        increment_id=generate_mock_order.increment_id).first()
    assert order.status == 'out_delivery'
    driver_controller.complete_order(generate_mock_order.increment_id)


@then('the order should be completed')
def order_complete(generate_mock_order):
    """Assert if order complete.

    params:
        generate_mock_order (fixture) - generates a mock order.

    Asserts:
        the status of the order.

    """
    time.sleep(10)
    order = SalesFlatOrder.objects.filter(
        increment_id=generate_mock_order.increment_id).first()
    assert order.status == 'complete'
