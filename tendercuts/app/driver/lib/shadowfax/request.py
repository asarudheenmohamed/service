import requests
import json
from .response import *

class ShadowFaxRequest(object):
    AUTH = "fbd68d4f8b841746df202362b1dab2fc26896915"
    URL = "https://hobbit.staging.shadowfax.in/api/v1/"
    CODE = "tendercuts001"

    def __init__(self, order):
        self.order = order

    def _prepare_headers(self):
        return {
                "Content-Type": "application/json",
                "Authorization": "Token " + self.AUTH
            }

    def create_order(self):
        shipping_address = [add for add in self.order.shipping_address.all()
            if add.address_type == "shipping"]
        shipping_address = shipping_address[0]

        data = {
            "client_code": self.CODE,
            "order_details": {
                "client_order_id": self.order.increment_id,
                "order_value": int(self.order.grand_total),
                # cod order should be false
                "paid": not self.order.is_cod,
            },
            "drop_details": {
                "name": self.order.customer_firstname + " " + \
                    self.order.customer_lastname,
                "contact_number": shipping_address.telephone,
                "house_number": shipping_address.fax or " ",
                "street": shipping_address.street,
                "locality": shipping_address.postcode,
                "city": shipping_address.city
            },
            "pickup_details": {
                "name": self.order.store.name,
                "contact_number": "9999999999",
                "locality": "600087", #shipping_address.telephone,
                "house_number": "2",
                "locality": "TN",
                "city": "chennai"
                # shipping_address.fax,
                # "street": shipping_address.street,
                # "locality": shipping_address.region + ", " + shipping_address.postcode,
                # "city": shipping_address.city,
                # "lati"
            },

        }

        endpoint = self.URL + "orders/"
        data = requests.post(
            endpoint,
            data=json.dumps(data),
            headers=self._prepare_headers())

        response = data.json()
        response = ShadowFaxCreateResponse(response)
        response.to_model().save()

        return response

