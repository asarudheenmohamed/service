"""Test cases for Notify customer controller."""
import pytest

from app.inventory.lib.notify_customer_controller import \
    NotifyCustomerController
from app.inventory.models import NotifyCustomer


@pytest.mark.django_db
class TestNotifyCustomerController:
    """To check Notify Customer Controller."""

    def test_get_customer_notify(self):
        """To check our fetched.

        Asserts:

            Check whether the order details are fetched or not.

        """
        controller = NotifyCustomerController()
        notify_customers = controller.get_customer_notify_obj()

        assert notify_customers[0].isnotified == False

        customers_notify = controller.get_avalible_notifies(notify_customers)

        username = customers_notify.keys()[0]
        product = customers_notify[username][0]

        obj = NotifyCustomer.objects.filter(
            customer__username=username,
            product_id=product[1],
            store_id=product[0])[0]

        assert obj != []

        controller.update_isnotified(notify_customers, customers_notify)

        assert obj.isnotified == True
