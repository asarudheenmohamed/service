from app.core.lib.exceptions import OrderNotFound
from .base import AbstractGateway
import ..models as models

from django.conf import settings
import logging
import requests
import requests.exceptions
import json

class GetSimplGateway(AbstractGateway):

    def __init__(self, log=None):
        super().__init__()
        self.api_secret = settings.PAYMENT_SIMPL["secret"]
        self.url = settings.PAYMENT_SIMPL["url"]

    def check_payment_status(self, orders):
        pass

    def update_order_with_payment(self, increment_id, transaction_token):
        sale_order = models.SalesFlatOrder.objects         \
                .filter(increment_id=increment_id)         \
                .prefetch_related("items")                 \
                .prefetch_related("payment")               \
                .prefetch_related("shipping_address")

        if (len(sale_order) == 0):
            raise OrderNotFound()

        items = []
        for item in sale_order.items:
            items.append({
                "sku": item.sku,
                "quantity": item.qty_ordered,
                "unit_price_in_paise": item.price * 100,
                "display_name": item.name
            })

        address = {
            "line1": sale_order.shipping_address.fax,
            "line2": sale_order.shipping_address.street,
            "city": sale_order.shipping_address.city,
            "state": sale_order.shipping_address.region,
            "pincode": sale_order.shipping_address.postcode
        }

        data = {
            "transaction_token": transaction_token,
            "amount_in_paise": sale_order.grand_total * 100,
            "order_id": sale_order.increment_id,
            "shipping_amount_in_paise": sale_order.shipping_amount * 100,
            "discount_in_paise": sale_order.discount_amount * 100,
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

        return response.data['status']