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

logging.getLogger().setLevel(logging.DEBUG)


@pytest.mark.django_db
class TestDriverTripController:

    def update_driver_position(self, django_user):
        """Create mock driver and mock trip."""
        user_obj = User.objects.get_or_create(
            username=django_user.username)[0]

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
            driver_order=mock_driver1,
            driver_position=driver_position, status='out_delivery')

        driver_position1 = DriverPosition.objects.create(
            driver_user=user_obj,
            latitude=12.9759,
            longitude=80.221)

        OrderEvents.objects.create(
            driver_order=mock_driver1,
            driver_position=driver_position1, status='completed')

        OrderEvents.objects.create(
            driver_order=mock_driver2,
            driver_position=driver_position, status='out_delivery')
        # create mock driver order events
        OrderEvents.objects.create(
            driver_order=mock_driver2,
            driver_position=driver_position1, status='completed')

        return mock_driver2, mock_trip

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

    @pytest.mark.django_db
    def test_driver_trip_complete(self, django_user):
        """Test driver trip complete.

        """
        user_obj = User.objects.get_or_create(
            username=django_user.username)[0]
        trip = TripController(driver=user_obj)
        driver_position = DriverPosition.objects.create(
            driver_user=user_obj,
            latitude=12.96095,
            longitude=80.24094)
        # create a mock driver and mock trip

        mock_driver, mock_trip = self.update_driver_position(user_obj)
        with mock.patch.object(cache, 'get_key', mock.Mock(return_value=mock_trip.id)):
            driver_trip = trip.check_and_complete_trip(
                mock_driver, driver_position)

        assert driver_trip.trip_completed == True

    @pytest.mark.django_db
    def test_compute_driver_trip_distance(self, django_user):
        """Test compute driver trip distance.

        Assarts:
          Checks the driver trip kms

        """
        user_obj = User.objects.get_or_create(
            username=django_user.username)[0]
        trip = TripController(driver=user_obj)

        # create a mock driver and mock trip
        mock_driver, mock_trip = self.update_driver_position(user_obj)

        driver_trip = trip.compute_driver_trip_distance(mock_trip)

        assert mock_trip.km_traveled == 4549
