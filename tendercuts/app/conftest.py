"""
Contains commons fixtures that needs to be shared accorss app
"""
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def rest():
    return APIClient()


@pytest.fixture
def auth_rest():
    from django.contrib.auth.models import User
    user = User.objects.get(username="u:18963")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def serializer():
    class EavSerializer():
        @classmethod
        def serialize(cls, data):
            obj = cls()
            for eav in data:
                print(eav)
                attr_name = eav['code']
                attr_value = eav['value']

                if (type(attr_value) is not list):
                    setattr(obj, attr_name, attr_value)
                else:
                    setattr(
                        obj,
                        attr_name,
                        EavSerializer.serialize(attr_value))
            return obj

@pytest.fixture(scope="session")
def generate_mock_order(magento):
    """
    1\ Creat cart
    2\ get and set customer
    3\ Add product
    4\ fetch and set shipping and billing address
    5\ shipping method
    6\ payment info

    """
    from app.core.models import SalesFlatOrder

    api = magento.api
    cart_id = api.cart.create("7")

    # customer = api.customer.info(16654)
    # staging
    #customer = api.customer.info(16034)
    customer = api.customer.info(18963)
    customer['mode'] = 'customer'
    api.cart_customer.set(cart_id, customer)

    product = api.catalog_product.info(196)
    product['qty'] = 1
    api.cart_product.add(cart_id, [product], "7", "7")

    address =  [{
        'mode': 'shipping',
        'firstname': customer['firstname'],
        'lastname': customer['lastname'],
        'street': 'street address',
        'city': 'city',
        'region': 'region',
        'telephone': '9908765678',
        'postcode': '600087',
        'country_id': '91',
        'is_default_shipping': 0,
        'is_default_billing': 0
        },
        {
        'mode': 'billing',
        'firstname': customer['firstname'],
        'lastname': customer['lastname'],
        'street': 'street address',
        'city': 'city',
        'region': 'region',
        'telephone': '9908765678',
        'postcode': '600087',
        'country_id': '91',
        'is_default_shipping': 0,
        'is_default_billing': 0
    }]

    api.cart_customer.addresses(cart_id, address)
    api.cart_shipping.method(cart_id, "tablerate_bestway")


    payment ={
            'po_number': None,
            'method' : 'payubiz',
            'cc_cid' : None,
            'cc_owner' : None,
            'cc_number': None,
            'cc_type': None,
            'cc_exp_year': None,
            'cc_exp_month': None}
    api.cart_payment.method(cart_id, payment)

    # place order
    order_id = api.cart.order(cart_id, "7", None)

    orders = SalesFlatOrder.objects.filter(increment_id=order_id)
    assert len(orders) == 1

    return orders[0]
