"""Order plased in test users."""
import pytest
from rest_framework.test import APIClient
import app.core.lib.magento as mage



@pytest.fixture(scope="session")
def test_user():
    return 18963

class GetUser:
    """Return in request User id."""
    def __init__(self):
        """initialize request user id.

        Returns:
            Get the user id from the request
            username contains u:18963 => 18963 is the magento IDS

        """
        self.user = self.request.user
        self.user_id = self.user.username.split(":")

        if len(self.user_id) < 1:
            self.user_id = None
        else:
            self.user_id = self.user_id[1]

        return self.user_id


class GenerateOrder(object):
    """Create sales order based on user id."""
    
    def __init__(self,customer_id):
        """Initialize in generate mork order object."""
        self.order = generate_order(customer_id)
    
def generate_order(customer_id):
    """Generate order base customer id.
    
    Params:
       custemer_id (int): user id
    
    1. Creat cart
    2. get and set customer
    3. Add product
    4. fetch and set shipping and billing address
    5. shipping method
    6. payment info
    
    Returns:
        return in user order object

    """
    from app.core.models import SalesFlatOrder
    conn = mage.Connector()
    api = conn.api
    cart_id = api.cart.create("7")

    # customer = api.customer.info(16654)
    # staging
    #customer = api.customer.info(16034)
    customer = api.customer.info(customer_id)
    customer['mode'] = 'customer'
    api.cart_customer.set(cart_id, customer)

    product = api.catalog_product.info(196)
    product['qty'] = 1
    api.cart_product.add(cart_id, [product], "7", "7")
    lastname = 'Test User'if not customer['lastname'] else customer['lastname']
    address =  [{
        'mode': 'shipping',
        'firstname': customer['firstname'],
        'lastname': lastname,
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
        'lastname': lastname,
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
