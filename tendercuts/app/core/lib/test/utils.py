"""Utilities for testing purposes.

Contains helper functions to place order.
"""

from datetime import datetime
# import dateutil.parser

import pytz
from rest_framework.test import APIClient

import app.core.lib.magento as mage

from app.core.models import SalesFlatOrder, SalesFlatOrderItem


class GenerateOrder(object):
    """Create sales order based on user id."""

    def __init__(self):
        """Initialize in generate mork order object."""
        pass

    def add_product(self, api, cart_id, product_id):
        for productname, qty in product_id:
                product = api.catalog_product.info(productname)
                product['qty'] = qty
                api.cart_product.add(cart_id, [product], "7", "7")


    def generate_order(self, customer_id, scheduled_order=False, product_id=[(196,1)]):
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
        # from app.core.models import SalesFlatOrder
        conn = mage.Connector()
        api = conn.api
        cart_id = api.cart.create("7")

        # customer = api.customer.info(16654)
        # staging
        #customer = api.customer.info(16034)
        customer = api.customer.info(customer_id)
        customer['mode'] = 'customer'
        api.cart_customer.set(cart_id, customer)

        self.add_product(api, cart_id, product_id)

        lastname = 'Test User'if not customer[
            'lastname'] else customer['lastname']
        address = [{
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

        payment = {
            'po_number': None,
            'method': 'payubiz',
            'cc_cid': None,
            'cc_owner': None,
            'cc_number': None,
            'cc_type': None,
            'cc_exp_year': None,
            'cc_exp_month': None}
        api.cart_payment.method(cart_id, payment)

        # place order
        order_id = api.cart.order(cart_id, "7", None)

        orders = SalesFlatOrder.objects.filter(increment_id=order_id)
        item_obj = SalesFlatOrderItem.objects.filter(order__increment_id=order_id)
        if scheduled_order:
            shedule_date = datetime.now()
            order = orders[0]
            order.order_now = 0
            order.deliverytype = 2
            order.scheduled_date = shedule_date.replace(
                hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
            order.scheduled_slot = 52
            order.save()
   
            items = item_obj[0]
            items.deliverydate = shedule_date.replace(
                    hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
            items.save()

        assert len(orders) == 1

        return orders[0]
