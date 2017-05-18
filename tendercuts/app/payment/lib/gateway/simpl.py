"""
GetSimpl implementation
"""

from app.core.lib.exceptions import OrderNotFound
from .base import AbstractGateway
from ... import models as models

from django.conf import settings
import logging
import requests
import requests.exceptions
import json


class GetSimplGateway(AbstractGateway):
    """
    Simpl gateway implemenatation
    """

    def __init__(self, log=None):
        """
        constructor
        """
        super(self.__class__, self).__init__()
        self.api_secret = settings.PAYMENT['SIMPL']["secret"]
        self.url = settings.PAYMENT['SIMPL']["url"]

    @property
    def magento_code(self):
        return "getsimpl"

    def check_payment_status(self, order_id, vendor_id):
        """
        Here we need to use the transaction token given by simpl to claim
        the transaction

        params:
            order_id (str): Incement Id
            vendor_id(str): Token given by simpl

        returns:
            status (boolean) True in case of sucess otherwise fail
        """
        sale_order = models.SalesFlatOrder.objects         \
            .filter(increment_id=order_id)         \
            .prefetch_related("items")                 \
            .prefetch_related("payment")               \
            .prefetch_related("shipping_address")

        if (len(sale_order) == 0):
            raise OrderNotFound()

        sale_order = sale_order[0]
        items = []
        for item in sale_order.items.all():
            items.append({
                "sku": item.sku,
                "quantity": int(item.qty_ordered),
                "unit_price_in_paise": int(item.price * 100),
                "display_name": item.name
            })

        shipping_address = sale_order.shipping_address.all()[0]
        address = {
            "line1": shipping_address.fax,
            "line2": shipping_address.street,
            "city": shipping_address.city,
            "state": shipping_address.region,
            "pincode": shipping_address.postcode
        }

        data = {
            "transaction_token": vendor_id,
            "amount_in_paise": int(sale_order.grand_total * 100),
            #"order_id": sale_order.increment_id,
            "shipping_amount_in_paise": int(sale_order.shipping_amount * 100),
            "discount_in_paise": int(sale_order.discount_amount * 100),
            "items": items,
            "shipping_address": address,
            "billing_address": address
        }

        headers = {
            "Authorization": self.api_secret,
            "Content-Type": "application/json"
        }

        response = requests.post(
            "{}/api/v1.1/transactions".format(self.url),
            headers=headers,
            data=json.dumps(data))

        response.raise_for_status()

        return response.json()['success']
