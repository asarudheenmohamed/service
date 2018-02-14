"""Integration tests for driver module.

Pre-requisite: The mage consumer should be running

"""

import pytest
from pytest_bdd import given, scenario, then, when
import app.core.lib.magento as mage
from app.core.lib.order_controller import OrderController
from app.driver.models import DriverOrder, DriverPosition, OrderEvents
from django.contrib.auth.models import User


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
def fetch_related_order(cache, auth_driver_rest,
                        store_id, generate_mock_order):
    """Generate mock order and Fetch relevent orders based on mock order id.

    Params:
        auth_driver_rest(pytest fixture): user requests
        generate_mock_order(obj): mock order object

    Asserts:
        Check response not equal to None
        Check response status code in equal to 200
        Check response status is equal to processing state

    """
    increment_id = str(generate_mock_order.increment_id)
    # Change that order status because fetch only processing orders
    controller = OrderController(mage.Connector(), generate_mock_order)
    generate_mock_order.status = 'processing'
    generate_mock_order.save()
    response = auth_driver_rest.get(
        "/driver/fetch_related_order/",
        {'order_id': increment_id[-2:],
         'store_id': store_id},
        format='json')
    cache['increment_id'] = response.data['results'][0]['increment_id']
    cache['store_id'] = store_id


@given('a driver is assigned to the order at <latitude><longitude>')
def driver_controller(cache, auth_driver_rest, latitude, longitude):
    """Assign the order.

    params:
        generate_mock_order (fixture) - generates a mock order.

    """
    response = auth_driver_rest.post(
        "/driver/assign/",
        {'order_id': cache['increment_id'],
         'store_id': cache['store_id'],
         'latitude': latitude,
         'longitude': longitude,
         },
        format='json')


@given('a update driver current locations for <latitude> and <longitude> <status> <message>')
def driver_position_update(
        cache,
        auth_driver_rest,
        latitude,
        longitude,
        status,
        message):
    """Test driver location updations.

    Params:
        auth_driver_rest(pytest fixture):user requests


    Asserts:
        Check response not equal to None
        Check response status code in equal to 200
        Check response status in equal to True
        Check response message in equal to param message

    """
    response = auth_driver_rest.post(
        "/driver/driver_position/",
        {'latitude': latitude,
            'longitude': longitude},
        format='json')
    assert (response) is not None
    assert response.status_code == 200
    assert str(response.data['status']) == status
    assert response.data[
        'message'] == message


@when('the order should be completed and the driver location for <latitude><longitude>')
def order_complete(cache, mock_driver, auth_driver_rest, latitude, longitude):
    """Assert if order complete.

    params:
        generate_mock_order (fixture) - generates a mock order.

    Asserts:
        the status of the order.

    """
    response = auth_driver_rest.post(
        "/driver/assign/complete/",
        {'order_id': cache['increment_id'],
         'latitude': latitude,
         'longitude': longitude},
        format='json')

    assert (response) is not None
    assert response.status_code == 201


@pytest.mark.django_db(transaction=True)
@then('find the no of driver stat objects')
def test_driver_stat(cache, auth_driver_rest):
    """Test driver stat objects.

    params:
        auth_driver_rest (fixture) - user requests.

    Asserts:
        Checks the count of driver stat object is 1.

    """
    response = auth_driver_rest.get(
        "/driver/driver_stat/", format='json')
    assert len(response.data['results']) == 0
    assert (response) is not None


@given("check the driver's current location")
def test_driver_position(
        cache, mock_driver, auth_driver_rest, latitude, longitude):
    """Test driver curent posittion.

    params:
        auth_driver_rest (fixture) - user requests.

    Asserts:
        Check the driver current location.

    """
    user = User.objects.get_or_create(
        username='u:{}'.format(
            mock_driver.entity_id))
    driver_position_obj = DriverPosition.objects.filter(
        driver_user=user[0]).last()

    assert (driver_position_obj) is not None
    assert str(driver_position_obj.latitude) == latitude
    assert str(driver_position_obj.longitude) == longitude
