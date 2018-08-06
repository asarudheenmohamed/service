"""Test cases for driver online controller."""

import pytest
from django.contrib.auth.models import User

from app.driver.lib.driver_online_controller import DriverOnlineController
from app.driver.models import DriverLoginLogout


@pytest.mark.django_db
class TestDriverOnlineController:
    """Test cases for Store Driver controller."""

    def test_driver_checkin(self, mock_driver):
        """Create the Driver checkin objects.

        Asserts:
            1.Check last created object is our user object
            2.Check status is True
        """
        user_obj = User.objects.get_or_create(
            username=mock_driver.dj_user_id)[0]

        controller = DriverOnlineController(user_obj)
        status = controller.driver_checkin()

        obj = DriverLoginLogout.objects.all().last()

        assert obj.driver == user_obj

        assert status is True

    def test_driver_checkout(self, mock_driver):
        """Update the Driver Check_Out time.

        Asserts:
            1.Check status is True
        """
        user_obj = User.objects.get_or_create(
            username=mock_driver.dj_user_id)[0]

        controller = DriverOnlineController(user_obj)

        controller = DriverOnlineController(user_obj)
        # create the check_in object with blank check_out time
        controller.driver_checkin()
        # update the check_out time for the created object
        status = controller.driver_checkout()

        assert status is True

    def test_driver_status(self, mock_driver):
        """Check Driver online status.

        Asserts:
            1.Check status is True
            2.Check status is False
        """
        user_obj = User.objects.get_or_create(
            username=mock_driver.dj_user_id)[0]

        controller = DriverOnlineController(user_obj)

        controller = DriverOnlineController(user_obj)
        # create object with blank check_out time
        controller.driver_checkin()
        # blank check_out time, so now driver is in online
        status = controller.driver_status()

        assert status is True

        # update check_out time for created object
        controller.driver_checkout()
        # check_out updated, therefore now driver is in offline
        status = controller.driver_status()

        assert status is False
