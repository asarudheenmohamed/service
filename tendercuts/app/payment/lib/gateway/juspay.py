from app.core.lib.exceptions import OrderNotFound
from .base import AbstractGateway
import ..models as models

import abc
import logging
import juspay

class JusPayGateway(AbstractGateway):
    API_KEY = "0F38CA55EAA0492987E8B5FB5635D223"

    def __init__(self, log=None):
        super().__init__()
        juspay.api_key = this.API_KEY

    def check_payment_status(self, orders):
        pass

    def create_order(self, increment_id):
        sale_order = models.SalesFlatOrder.filter(increment_id=increment_id)

        if (len(sale_order) == 0):
            raise OrderNotFound()

        phno = CustomerEntityVarchar.objects.filter(
            Q(attribute_id=149) & Q(entity_id=sale_order.customer_id))
        
        if (len(phno) > 0):
            # TODO: need to pass in phno
            phno = phno[0].value

        juspay.Orders.create(
            order_id=increment_id,
            amount=str(round(sale_order.grand_total, 2)),
            currency='INR',
            customer_id=sale_order.customer_id,
            customer_email=sale_order.customer_email,
            customer_phone=phno,
            return_url='https://staging.tendercuts.in:82/payment/juspay/handleresponse',
            description='Tendercuts Order',
        )
