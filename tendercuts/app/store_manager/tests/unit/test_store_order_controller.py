"""Test cases for store order controller."""
import pytest
from django.contrib.auth.models import User

from app.driver.models import DriverPosition
from app.store_manager.lib.store_order_controller import StoreOrderController


@pytest.mark.django_db
class TestStoreOrderController:
    """Test cases for store order controller."""

    @pytest.mark.django_db
    def test_driver_location(self, generate_mock_order):
        """Check driver's current location.

        Asserts:
            Check Driver's current latitude & longitude.

        """
        user_obj, status = User.objects.get_or_create(username="u:1234")

        past_record = DriverPosition.objects.create(
            driver_user=user_obj,
            latitude=12.9229,
            longitude=80.1275)
        recent_record = DriverPosition.objects.create(
            driver_user=user_obj,
            latitude=12.9759,
            longitude=80.221)

        controller = StoreOrderController()
        current_location = controller.get_driver_location(user_obj)

        assert recent_record.latitude == current_location.latitude
        assert recent_record.longitude == current_location.longitude
