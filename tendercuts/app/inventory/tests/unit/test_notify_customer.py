"""Test cases for Notify customer controller."""
import datetime

import pytest

from app.core.models import Graminventory, GraminventoryLatest
from app.inventory.lib.notify_customer_controller import \
    NotifyCustomerController
from app.inventory.models import NotifyCustomer


@pytest.mark.django_db
class TestNotifyCustomerController:
    """To check Notify Customer Controller."""

    def test_get_customer_notify(self, auth_rest):
        """To check our fetched.

        Asserts:

            Check whether the order details are fetched or not.

        """
        response = auth_rest.post(
            "/inventory/notify_me/",
            {'store_id': 1,
             'product_id': 221,
             },
            format='json')

        assert response.status_code == 201

        controller = NotifyCustomerController()
        notify_customers = controller.get_customer_notify_obj()

        obj = notify_customers.last()

        assert obj.is_notified == False

        # To check last Notifycustomer's products from Graminventory
        inv = Graminventory.objects.filter(
            date=datetime.date.today(),
            product_id=obj.product_id,
            store_id=obj.store_id)

        # If it is not available, create it with our notify products
        if not inv:
            inv = Graminventory(
                date=datetime.date.today(),
                product_id=obj.product_id,
                store_id=obj.store_id,
                qty=10).save()

        customers_notify = controller.get_avalible_notifies(notify_customers)

        # To check created products are added to our customers's_notify list
        status = (obj.product_id, obj.store_id) in customers_notify.get(
            obj.customer.id)

        assert status == True

        obj = NotifyCustomer.objects.get(id=obj.id)
        # To check is_notified is updated for Notify listed customers

        assert obj.is_notified == True
