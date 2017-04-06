import requests
import json
from .response import *


class ShadowFaxRequest(object):
    AUTH = "23bfc90a731d04ced956302c903ab8ea6b96b60a"
    URL = "http://api.shadowfax.in/api/v1/"
    CODE = "tc00001"
    _ADDRESS = {
        "porur": {
            "house_number": "162",
            "street": "Kunarthur Main Road",
            "address": "Gerugambakkam,Chennai-600122",
            "phone": "9962123577",
            "latitude": "13.017100",
            "longitude": "80.138710"
        },
        "tambaram": {
            "house_number": "103/254",
            "street": "Bharathamatha Street",
            "address": "East Tambram,Chennai-600059",
            "phone": "9962123577",
            "latitude": "12.932701",
            "longitude": "80.128456"
        },
        "thoraipakkam": {
            "house_number": "667",
            "street": "Venkateswara Avenue",
            "address": "OMR,PTC-Thooraipakkam,chennai-600097",
            "phone": "9962123577",
            "latitude": "12.932999",
            "longitude": "80.232793"
        },
        "adayar": {
            "house_number": "192",
            "street": "New No:8,Arangannal Salai,Canal Bank Road",
            "address": "kashturibai Nagar,Adyar,Chennai-600020",
            "phone": "9962123577",
            "latitude": "13.006194",
            "longitude": "80.248289"
        },
        "arumbakkam": {
            "house_number": "2A",
            "street": "Visalatchi Street",
            "address": "Balavinayager Nagar,Arumbakkam,Chennai-600106",
            "phone": "9962123577",
            "latitude": "13.066978",
            "longitude": "80.210991"
        }
    }

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
        house_no = self._ADDRESS[
            "" + self.order.store.name + ""]['house_number']
        street_name = self._ADDRESS["" + self.order.store.name + ""]['street']
        location = self._ADDRESS["" + self.order.store.name + ""]['address']
        lattitude = self._ADDRESS["" + self.order.store.name + ""]['latitude']
        longitude = self._ADDRESS["" + self.order.store.name + ""]['longitude']
        phone = self._ADDRESS["" + self.order.store.name + ""]['phone']

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
                "contact_number": phone,
                "latitude": lattitude,
                "longitude": longitude,
                "house_number": house_no,
                "street": street_name,
                "locality": location,
                "city": "chennai"
                # shipping_address.fax,
                # "street": shipping_address.street,
                # "locality": shipping_address.region +
                # ", " + shipping_address.postcode,
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
