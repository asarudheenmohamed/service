"""Integration tests for driver module.

Pre-requisite: The mage consumer should be running

"""

import time

import pytest
from pytest_bdd import given, scenario, then, when

from app.core.models import SalesFlatOrder
from app.driver.lib.driver_controller import DriverController


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


@given('Fetch related order by <store_id>')
def fetch_related_order(cache, auth_rest, store_id, generate_mock_order):
    """Generate mock order and Fetch relevent orders based on mock order id.

    Params:
        auth_rest(pytest fixture): user requests
        generate_mock_order(obj): mock order object

    Asserts:
        Check response not equal to None
        Check response status code in equal to 200
        Check response status is equal to processing state

    """
    obj = SalesFlatOrder.objects.filter(
        increment_id=generate_mock_order.increment_id)
    obj = obj[0]
    obj.status = 'Processing'
    obj.save()

    increment_id = str(generate_mock_order.increment_id)

    inc_id = list(increment_id)
    increment_id = increment_id.split(inc_id[2])

    response = auth_rest.get(
        "/driver/fetch_related_order/",
        {'order_id': increment_id[-1],
            'store_id': store_id},
        format='json')
    cache['increment_id'] = response.data['results'][0]['increment_id']
    cache['store_id'] = store_id


@given('a driver is assigned to the order')
def driver_controller(cache, auth_rest, mock_user):
    """Assign the order.

    params:
        mock_user (fixture) - generates a driver object
        generate_mock_order (fixture) - generates a mock order.

    """
    response = auth_rest.post(
        "/driver/assign/",
        {'order_id': cache['increment_id'],
         'store_id': cache['store_id']},
        format='json')


@when('the driver completes the order')
def complete_order(mock_user, cache):
    """Complete the order.

    Asserts:
        Verify if the order is set in out_delivery stat

    params:
        driver_controller (fixture) - generates a driver object.
        generate_mock_order (fixture) - generates a mock order.

    """
    time.sleep(5)
    order = SalesFlatOrder.objects.filter(
        increment_id=cache['increment_id']).first()
    assert order.status == 'out_delivery'
    controller = DriverController(mock_user)
    controller.complete_order(cache['increment_id'])


@then('the order should be completed')
def order_complete(cache, auth_rest):
    """Assert if order complete.

    params:
        generate_mock_order (fixture) - generates a mock order.

    Asserts:
        the status of the order.

    """
    response = auth_rest.post(
        "/driver/assign/complete/",
        {'order_id': cache['increment_id']},
        format='json')

    assert (response) is not None
    assert response.status_code == 201
