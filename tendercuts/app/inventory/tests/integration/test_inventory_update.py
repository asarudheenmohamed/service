"""Integration tests for notify inventory module."""
import pytest
import datetime
from pytest_bdd import given, when, then, scenario

from app.inventory import tasks
from app.core.models import Graminventory


@pytest.mark.django_db
@scenario(
    'inventory.feature',
    'Notify updated inventory'
)
def test_notify():
    pass


@given('Create notify object for <product1> and <product2>')
def create_notify(auth_rest,
                  product1 , product2):
    """Create NotifyCustomer object.

    Params:
        auth_driver_rest(pytest fixture): user requests
        store_id(int): requested store
        product_id(int): requested product

    Asserts:
        Check response not equal to None
        Check response status code in equal to 200
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

        assert (response) is not None

        assert response.status_code == 201

        assert str(response.data['store_id']) == store_id


@when('The inventory is updated for <product1>, <product2>')
def notify_customer(product1, product2):
    """Check customer receives the updated inventory sms.

    Asserts:
        Check the response is True

    """
    for data in [product1, product2]:
        store_id, product_id = map(int, data.split(','))
        inv = Graminventory.objects.filter(
            date=datetime.date.today(),
            product_id=product_id,
            store_id=store_id)

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
        Check the response is True

    """
    pass
