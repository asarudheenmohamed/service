"""Test cases for Test notify customer controller."""
import pytest

from app.inventory.lib import NotifyCustomerController


@pytest.mark.django_db
class TestNotifyCustomerController:
    """Test cases."""

    @pytest.mark.parametrize("product,store", [(195, 1)])
    def test_create_notify(self, mock_user, product, store):
        """To check the customer notify order.

        Asserts:

            Check whether the notify objects are created or not.

        """
        user_name = ("{}:{}".format("u", mock_user.entity_id))
        controller = NotifyCustomerController()
        obj = controller.create_notify(user_name, 1, 195)

        assert obj.product_id == product

        assert obj.store_id == store

        assert obj.customer.username == user_name
