"""All order controller related actions."""
import logging
import dateutil.parser
import datetime
from django.db.models import Sum

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder, SalesFlatOrderItem

logger = logging.getLogger(__name__)


class OrderDataController(object):
    """Order Data controller."""

    def __init__(self, order):
        """Constructor."""
        self.order = order

    def order_details(self, order_id):
        """Fetch the order details.

        Params:
            order_id(str):Customer placed order_id

        Returns:
            Returns params_data

        """
        orders = SalesFlatOrder.objects.filter(increment_id=order_id)

        params_data = []
        for order in orders:
            shipping_address = order.shipping_address.all()[0]
            user = CustomerSearchController.load_basic_info(order.customer_id)
            params = {
                "increment_id": order.increment_id,
                "created_at": str(order.created_at),
                "total_amount": float(order.grand_total),
                "subtotal_amount": float(order.subtotal),
                "shipping_amount": float(order.shipping_amount),
                "discount_amount": float(order.discount_amount),
                "discount_description": order.discount_description or '',
                "payment_method": order.payment.all()[0].method,
                "medium": order.medium,

                "customer": {
                    "partner_name": order.customer_firstname,
                    "phone": user[2],
                    "email": order.customer_email
                },
                "shipping_address": {
                    "street": shipping_address.street,
                    "street2": shipping_address.region or "",
                    "city": shipping_address.city,
                },
                "store":  order.store.code

            }

            for item in order.items.all():
                params.setdefault("product_list", []).append({
                    "sku": item.sku.strip(),
                    "ordered_qty": float(item.qty_ordered),
                    "weight": float(item.weight),
                    "unit_price": float(item.price),
                    "total_amount": float(item.row_total),
                    "discount_amount": float(item.discount_amount or 0)

                })
            params_data.append(params)

            logger.info("Getting order details list of order_id:{}".format(
                order_id))

        return params_data


class StoreOrderController(object):
    """Order Data controller."""

    def __init__(self, store):
        """Constructor."""
        self.store = store

    def store_details(self, store_id, deliverydate, sku):
        """Fetch the store order details.

        Params:
            store_id(int) : Store id
            deliverydate(DateTimeField): Order's delivery date
            sku(str) : Product sku name

        Returns:
            Returns sku_data

        """
        deliverydate = dateutil.parser.parse(deliverydate)
        order_data = SalesFlatOrderItem.objects.filter(
            deliverydate__range=(
                deliverydate,
                deliverydate + datetime.timedelta(days=1)),
            order__store_id=store_id)  \
            .values('sku').annotate(Sum('qty_ordered'))

        sku_data = []
        sku_orders = order_data.filter(sku=sku)
        for sku_order in sku_orders:
            sku_list = {'SKU': sku_order['sku'],
                        'Qty': sku_order['qty_ordered__sum']}
            sku_data.append(sku_list)

        return sku_data
