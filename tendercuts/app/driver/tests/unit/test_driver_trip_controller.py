"""Test Driver trip functionalities."""
import logging

import mock
import pytest
from django.contrib.auth.models import User

from app.core.lib import cache
from app.core.models import SalesFlatOrder
from app.driver.lib.trip_controller import TripController
from app.driver.models import (DriverOrder, DriverPosition, DriverTrip,
                               OrderEvents)
from datetime import datetime

from app.driver.lib import DriverTripController
logging.getLogger().setLevel(logging.DEBUG)


@pytest.mark.django_db
class TestDriverTripController:

    @pytest.mark.django_db
    def test_driver_trip_create(self, django_user):
        user_obj = User.objects.get_or_create(
            username=django_user.username)[0]
        trip = TripController(driver=user_obj)

        driver_position = DriverPosition.objects.create(
            driver_user=user_obj,
            latitude=12.96095,
            longitude=80.24094)
        with mock.patch.object(cache, 'get_key', mock.Mock(return_value=None)):
            mock_driver = DriverOrder.objects.create(
                driver_user=user_obj, increment_id=2)
            driver_trip = trip.check_and_create_trip(
                mock_driver, driver_position)

        assert len(driver_trip.driver_order.all()) == 1

        # now let's mock the cache fetch
        with mock.patch.object(cache, 'get_key', mock.Mock(return_value=driver_trip.id)):
            mock_driver = DriverOrder.objects.create(
                driver_user=user_obj, increment_id=3)
            driver_trip = trip.check_and_create_trip(
                mock_driver, driver_position)

        assert len(driver_trip.driver_order.all()) == 2

    def test__complete_trip(self, django_user):
        """Test completed trip."""
        user_obj = User.objects.get_or_create(
            username=django_user.username)[0]
        driver_trip = DriverTrip.objects.create(driver_user=user_obj)

        trip = TripController(driver=user_obj)

        driver_order_events = trip._complete_trip(driver_trip)

        trip = DriverTrip.objects.filter(id=driver_trip.id)

        assert len(trip) is 0
