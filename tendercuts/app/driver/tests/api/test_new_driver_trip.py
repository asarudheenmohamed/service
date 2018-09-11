import pytest
from app.driver.lib import DriverTripController
from django.contrib.auth.models import User


@pytest.fixture
@pytest.mark.django_db
def mock_new_driver():
    return User.objects.create_user(
        username="test", email="test@test.com",
        password='test')


@pytest.mark.django_db
def test_get_or_create_trip_api(auth_new_driver_rest):
    """Verify if we can get/create new trip.
    Complete the api & retrieve it.
    """

    response = auth_new_driver_rest.get(
        "/driver/trip/current/", format='json')
    assert len(response.json()['trip_created_time']) > 0

    response = auth_new_driver_rest.get(
        "/driver/trip/current/start/", format='json')
    assert response.json()['status'] is True
