import pytest
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
import base64
from rest_framework import HTTP_HEADER_ENCODING



@pytest.fixture
def rest():
    return APIClient()


@pytest.fixture
def username():
    return "9908765678"


@pytest.fixture
def password():
    return "test"


@pytest.fixture
def auth(username, password):
    credentials = ('%s:%s' % (username, password))
    base64_credentials = base64.b64encode(
        credentials.encode(HTTP_HEADER_ENCODING)
    ).decode(HTTP_HEADER_ENCODING)

    auth = 'Basic %s' % base64_credentials

    return auth

@pytest.fixture(scope="module")
def generate_mock_order(magento):
    """
    1\ Creat cart
    2\ get and set customer
    3\ Add product
    4\ fetch and set shipping and billing address
    5\ shipping method
    6\ payment info

    """
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
    return 1

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

    return order_id
