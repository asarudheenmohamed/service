"""Test cases for store order controller."""
import pytest
from django.contrib.auth.models import User

from app.driver.models import DriverPosition
from app.store_manager.lib.store_order_controller import StoreOrderController
from app.core.models import SalesFlatOrder


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

    @pytest.mark.django_db
    def test_store_manager_assign_orders(self, mock_driver):
        """Check store manager assign orders.

        Asserts:
            Check the assign driver id.

        """
        user_obj, status = User.objects.get_or_create(username="u:1234")

        data = {'driver_user': user_obj.id,
                'driver_order': [2134234, 345436556]}

        controller = StoreOrderController()
        obj = controller.store_manager_assign_orders(data)

        assert obj.driver_user_id == user_obj.id

    @pytest.mark.django_db
    def test_update_driver_details(self, mock_driver, generate_mock_order):
        """Check update driver details.

        Asserts:
            Check the mocking driver username and mobilenumber.

        """
        user_obj, status = User.objects.get_or_create(
            username=mock_driver.dj_user_id)

        controller = StoreOrderController()
        obj = controller._update_driver_details(
            user_obj, [generate_mock_order.increment_id])

        order_obj = SalesFlatOrder.objects.filter(
            increment_id=generate_mock_order.increment_id).last()

        assert order_obj.driver_number == mock_driver._flat['mobilenumber']
        assert order_obj.driver_name == mock_driver._flat['firstname']
