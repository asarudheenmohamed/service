from .base import AbstractGateway
from app.payment import models as models
import requests
import hashlib
import json
import logging

class Payu(AbstractGateway):
    MERCHANT_ID = "U6KiaG3M"
    KEY = "xV0BSL"

    def filter_orders(self, orders, threshold=60*15):
        # get only payu orders
        orders = [order for order in orders 
            if order.is_payu and order.time_elapsed().seconds > threshold]

        return orders

    def check_payment_status(self, orders):
        COMMAND = "verify_payment"

        wsUrl = "https://info.payu.in/merchant/postservice?form=2" #For live server
        # if self.test:
        #     wsUrl = "https://test.payu.in/merchant/postservice.php?form=2"

        order_map = {order.increment_id: order 
                for order in orders}
        order_ids = list(order_map.keys())

        hash_val = hashlib.sha512("{}|{}|{}|{}".format(
                self.KEY,
                COMMAND,
                "|".join(order_ids),
                self.MERCHANT_ID))

        data = {
            'key': self.KEY ,
            'hash': hash_val.hexdigest(),
            'var1': "|".join(order_ids),
            'command': COMMAND}

        res = requests.post(wsUrl, data=data, timeout=30)
        res.raise_for_status()

        self.log.info("Payu response: {}".format(
            res.text))
        payu_status = []
        try:
            response = res.json()
            # response = [response] if type(response) is not list else response
            for inc_id, status in response['transaction_details'].items():
                model = models.PaymentStatusResponse.from_payu_status(
                    order_map[inc_id],
                    status)
                payu_status.append(model)

        except ValueError as e:
            self.log.exception(str(e))
        except KeyError as e:
            self.log.exception(str(e))

        return payu_status
