"""Integration tests for notify inventory module."""
import datetime
import time
import pytest
from pytest_bdd import given, scenario, then, when

from app.core.models import Graminventory
from app.inventory import tasks
from app.inventory.models import NotifyCustomer


@pytest.mark.django_db
@scenario(
    'inventory.feature',
    'Notify the customer Once the inventory updated'
)
def test_notify():
    """Check the NotifyCustomer."""
    pass


@given('Create notify object for <product1> and <product2>')
def create_notify(auth_rest, mock_django_user, product1, product2):
    """Create NotifyCustomer object.

    Params:
        auth_driver_rest(pytest fixture): user requests
        product1(int): store_id1, product_id1
        product2(int): store_id2, product_id2

    Asserts:
        Check response not equal to None
        Check response status code in equal to 201
        Check response store id is equal to given store id

    """
    for data in [product1, product2]:
        store_id, product_id = data.split(',')

        response = auth_rest.post(
            "/inventory/notify_me/",
            {'store_id': store_id,
             'product_id': product_id,
             },
            format='json')

        assert response.status_code == 201, response.json()

        assert str(response.data['store_id']) == store_id


@when('The inventory is updated for <product1>, <product2>')
def notify_customer(product1, product2):
    """Check customer receives the updated inventory sms.

    Params:
        product1(int): store_id1, product_id1
        product2(int): store_id2, product_id2

    Asserts:
        Check the response is True

    """
    for data in [product1, product2]:
        store_id, product_id = map(int, data.split(','))
        # To get Notifycustomer products from Graminventory
        inv = Graminventory.objects.filter(
            date=datetime.date.today(),
            product_id=product_id,
            store_id=store_id)
        # If it is not available create the inventory
        if not inv:
            inv = Graminventory(
                date=datetime.date.today(),
                product_id=product_id,
                store_id=store_id,
                qty=10).save()

    response = tasks.notification_sms.apply()
    status = response.get()
    assert status == True


@then('Notify customer object will set as notified')
def update_isnotified():
    """Check Once receive the SMS NotifyCustomer obj marked as notified or not.

    Asserts:
        Check the obj.is_notified is True

    """
    obj = NotifyCustomer.objects.all().last()
    # Check our created NotifyCustomer object marked as notified or not

    assert obj.is_notified == True
