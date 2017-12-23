from app.driver.lib.trip_controller import TripController
from app.driver.models import DriverOrder, DriverTrip
from app.core.lib import cache

import pytest
import mock

import logging
logging.getLogger().setLevel(logging.DEBUG)


@pytest.mark.django_db
def test_driver_trip_create():
    trip = TripController()

    with mock.patch.object(cache, 'get_key', mock.Mock(return_value=None)):
        mock_driver = DriverOrder.objects.create(driver_id=1, increment_id=2)
        driver_trip = trip.check_and_create_trip(mock_driver)

    assert len(driver_trip.driver_order.all()) == 1

    # now let's mock the cache fetch
    with mock.patch.object(cache, 'get_key', mock.Mock(return_value=driver_trip.id)):
        mock_driver = DriverOrder.objects.create(driver_id=1, increment_id=3)
        driver_trip = trip.check_and_create_trip(mock_driver)

    assert len(driver_trip.driver_order.all()) == 2


@pytest.mark.django_db
def test_driver_trip_complete():
    trip = TripController()

    mock_driver1 = DriverOrder.objects.create(driver_id=1, increment_id=100000003)
    mock_driver2 = DriverOrder.objects.create(driver_id=1, increment_id=100000004)
    mock_trip = DriverTrip.objects.create()
    mock_trip.driver_order.add(*[mock_driver1, mock_driver2])

    with mock.patch.object(cache, 'get_key', mock.Mock(return_value=mock_trip.id)):
        driver_trip = trip.check_and_complete_trip(mock_driver2)

    assert driver_trip.trip_complete == True

