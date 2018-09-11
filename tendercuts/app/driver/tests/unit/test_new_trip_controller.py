import pytest
from app.driver.lib import DriverTripController


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
