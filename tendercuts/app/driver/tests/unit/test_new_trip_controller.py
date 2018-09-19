from datetime import datetime

from django.contrib.auth.models import User

import pytest
from app.core.lib import cache
from app.core.models import SalesFlatOrder
from app.driver.lib import DriverTripController
from app.driver.lib.trip_controller import TripController
from app.driver.models import (DriverOrder, DriverPosition, DriverTrip,
                               OrderEvents)


@pytest.mark.django_db
def test_get_or_create_trip(mock_new_driver):
    """Verify if we can get/create new trip"""
    trip = DriverTripController.get_or_create_trip(mock_new_driver)
    assert trip.status == 0

    new_trip = DriverTripController.get_or_create_trip(mock_new_driver)
    assert new_trip.id == trip.id


@pytest.mark.django_db
def test_completed_trips(mock_new_driver):
    """Verify if we can retrieve completed trips"""
    trip = DriverTripController.get_or_create_trip(mock_new_driver)
    assert trip.status == 0

    trips = DriverTripController.get_completed_trips(mock_new_driver)
    assert len(trips) == 0

    trip.status = 2
    trip.save()

    trips = DriverTripController.get_completed_trips(mock_new_driver)
    assert len(trips) == 1


def update_driver_position(django_user):
    """Create mock driver and mock trip."""
    user_obj = User.objects.get_or_create(
        username="asar")[0]

    order_object = SalesFlatOrder.objects.filter(status='processing')[:2]

    # mock driver assign order 1
    mock_driver1 = DriverOrder.objects.create(
        driver_user=user_obj, increment_id=order_object[0].increment_id)

    # mock driver assign order 2
    mock_driver2 = DriverOrder.objects.create(
        driver_user=user_obj, increment_id=order_object[1].increment_id)

    # create mock driver trip
    mock_trip = DriverTrip.objects.create(driver_user=user_obj)
    mock_trip.driver_order.add(*[mock_driver1, mock_driver2])

    # create mock driver position
    driver_position = DriverPosition.objects.create(
        driver_user=user_obj,
        latitude=12.96095,
        longitude=80.24094)

    OrderEvents.objects.create(
        driver=mock_driver1,
        driver_position=driver_position, status='out_delivery')

    driver_position1 = DriverPosition.objects.create(
        driver_user=user_obj,
        latitude=12.9759,
        longitude=80.221)

    OrderEvents.objects.create(
        driver=mock_driver1,
        driver_position=driver_position1, status='completed')

    OrderEvents.objects.create(
        driver=mock_driver2,
        driver_position=driver_position, status='out_delivery')
    # create mock driver order events
    order_events = OrderEvents.objects.create(
        driver=mock_driver2,
        driver_position=driver_position1, status='completed')

    return mock_driver1, mock_driver2, mock_trip, order_events


@pytest.mark.django_db
def test__get_way_points(django_user):
    """Test driver way points."""
    starting_time = datetime.now()
    user_obj = User.objects.get_or_create(
        username=django_user.username)[0]
    controller = DriverTripController(user_obj)
    driver_order = DriverOrder.objects.create(
        driver_user=user_obj,
        increment_id=1111111)
    driver_position = DriverPosition.objects.create(
        driver_user=user_obj, latitude=11.24525, longitude=80.22222)
    order_events = OrderEvents.objects.create(
        driver=driver_order,
        driver_position=driver_position)

    driver_order_events = controller._get_way_points(
        starting_time, [order_events], user_obj)

    assert driver_order_events[0] == '11.24525,80.22222'


@pytest.mark.django_db
def test_add_driver_orders_and_sequence_number(django_user):
    """Test trip id based driver order update method and sequence number update.
    Assert:
     Checks the trip assign order
    """
    # mock order id
    increment_id = SalesFlatOrder.objects.all().last().increment_id

    user_obj = User.objects.get_or_create(
        username=django_user.username)[0]

    driver_order = DriverOrder.objects.create(
        driver_user=user_obj,
        increment_id=increment_id)
    trip = DriverTrip.objects.create(driver_user=user_obj)

    controller = DriverTripController(trip)
    controller.add_driver_orders_and_sequence_number(driver_order)

    trip = DriverTrip.objects.get(driver_user=user_obj)

    assert trip.driver_order.all().last() == driver_order

    order = SalesFlatOrder.objects.filter(increment_id=increment_id).last()

    # checks the order sequence number
    assert order.sequence_number == 1


@pytest.mark.django_db
def test_compute_driver_trip_distance(django_user):
    """Test compute driver trip distance.

    Assarts:
      Checks the driver trip kms

    """
    user_obj = User.objects.get_or_create(
        username=django_user.username)[0]

    # create a mock driver and mock trip
    mock_driver1, mock_driver2, mock_trip, order_events = update_driver_position(
        user_obj)

    trip = DriverTripController(mock_trip)
    driver_trip = trip.compute_driver_trip_distance()

    assert (5500 < mock_trip.km_travelled < 5600)


@pytest.mark.django_db
def test_update_sequence_number(django_user):
    """Test order delivered sequence number.
    params:
        django_user (fixture) - django user obj.

    """
    user_obj = User.objects.get_or_create(
        username=django_user.username)[0]
    mock_driver1, mock_driver2, mock_trip, order_events = update_driver_position(
        user_obj)

    order_obj = SalesFlatOrder.objects.filter(
        increment_id__in=[
            mock_driver1.increment_id,
            mock_driver2.increment_id])

    sequence_number = 1
    for i in order_obj:
        i.sequence_number = sequence_number
        i.save()
        sequence_number += 1

    trip = DriverTripController(mock_trip)
    trip.update_sequence_number(order_obj[0].increment_id, 1)
    order = SalesFlatOrder.objects.filter(
        increment_id__in=[
            mock_driver1.increment_id,
            mock_driver2.increment_id]).values('sequence_number', 'increment_id')

    assert int(order[0]['sequence_number']) == 2
    assert int(order[1]['sequence_number']) == 1
