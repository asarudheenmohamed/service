"""Integration tests for notify inventory module."""
import pytest

from app.inventory import tasks


@pytest.mark.django_db
@scenario(
    'inventory.feature',
    'Notify updated inventory'
 )
def test_notify():
    pass


@given('Create notify object for store <store_id> and product <product_id>')
def create_notify(auth_rest,
                  store_id, product_id):
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
    response = auth_rest.post(
        "/inventory/notify_me/",
        {'store_id': store_id,
         'product_id': product_id,
         },
        format='json')

    assert (response) is not None

    assert response.status_code == 200

    assert str(response.data['store_id']) == store_id


@when('Once the inventory updated customer will receive the SMS')
def notify_customer():
    """Check customer receives the updated inventory sms.

    Asserts:
        Check the response is True

    """
    response = tasks.notification_sms.apply()

    status = response.get()

    assert status == True


@then('Notify customer object will set as notified')
def update_isnotified():
    """Check Once receive the SMS NotifyCustomer obj marked as notified or not.

    Asserts:
        Check the response is True

    """
    response1 = tasks.notification_sms.apply()

    assert response1.get() == True
