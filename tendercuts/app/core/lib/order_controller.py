"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging

from django.utils import timezone
from app.core.models.sales_order import (SalesFlatOrderGrid, SalesFlatOrder, SalesFlatOrderAddress,
                                         SalesFlatOrderStatusHistory)

from app.core.lib.communication import Mail

from .magento import Connector

logger = logging.getLogger(__name__)


class OrdersController(object):
    """
    Update order status
    """

    def __init__(self, magento_conn):
        super(OrdersController, self).__init__()
        self.mage = magento_conn

    def processing(self, orders):
        """The order status pending to processing state."""
        orders = [{'increment_id': order.increment_id} for order in orders]
        response_data = self.mage.api.tendercuts_order_apis.updateProcessing(
            orders)
        logger.info(response_data)


class OrderController(object):
    """
    Update order status
    """

    def __init__(self, magento_conn, order):
        super(OrderController, self).__init__()
        self.order = order
        self.mage = magento_conn

    def processing(self):
        """The order status pending to processing state."""
        response_data = self.mage.api.tendercuts_order_apis.updateProcessing(
            [{'increment_id': self.order.increment_id}])
        logger.info(
            'This order:{} was changed to out for delivery'.format(
                self.order.increment_id))

    def out_delivery(self):
        """The order status processing to out for delivery."""
        try:
            response_data = self.mage.api.tendercuts_order_apis.updateOutForDelivery(
                [{'increment_id': self.order.increment_id}])
            logger.info(
                'This order:{} was changed to out for delivery'.format(
                    self.order.increment_id))
        except Exception as msg:
            Mail().send(
                "reports@tendercuts.in",
                ["tech@tendercuts.in"],
                "[CRITICAL] Error in Order OutDelivery API",
                repr(msg))

        response_data

    def complete(self):
        """
        Using the megento custom API here, as we need to triggers observers in magento for
        reward and credit.

        """
        try:
            response_data = self.mage.api.tendercuts_order_apis.completeOrders(
                [{'increment_id': self.order.increment_id}])
        except Exception as msg:
            Mail().send(
                "reports@tendercuts.in",
                ["tech@tendercuts.in"],
                "[CRITICAL] Error in Order Complete API",
                repr(msg))

        return response_data

    def cancel(self):
        """
        Triggring soap api here to enable any Mage observer
        """
        logger.debug("Cancelling {}".format(self.order.increment_id))

        status = self.mage.api.sales_order.cancel(
            self.order.increment_id)

        if status:
            self.order.grid.status = "canceled"
            self.order.grid.save()

            logger.info("Cancelled {}".format(self.order.increment_id))
        else:
            logger.info("Unable to Cancel {}".format(self.order.increment_id))

        return status

    def payment_success(self, is_comment=None):
        """If payment in successful, update status.

        1. Update status as "pending" for express
        2. Update status as sch_order for scheduled
        3. Update as pending for split order
        4. Grid also needs to be updated.
        """
        # express delivery
        if self.order.deliverytype == 1:
            status = "pending"
        # sch
        elif self.order.deliverytype == 2:
            status = "scheduled_order"
        # split
        else:
            status = "pending"

        self.order.status = status
        self.order.save()

        if getattr(self.order, "grid", None):
            self.order.grid.status = "pending"
            self.order.grid.save()

        if is_comment:
            # update order status history
            SalesFlatOrderStatusHistory.objects.create(
                parent=self.order,
                status=status,
                created_at=timezone.now(),
                comment=is_comment,
                is_customer_notified=1,
                is_visible_on_front=1,
                entity_name='order')

    def update_payment_status(self):
        """Update the payment_received flag.

        Ideally this should be merged with payment_sucess eventually
        DEPRECATED
        """
        self.order.payment_received = 1
        self.order.save()


class OrderAddressController():

    shipping_address = None  # type: SalesFlatOrderAddress
    order = None  # type: SalesFlatOrder

    def __init__(self, order):
        self.order = order

        self.shipping_address = self.order.shipping_address.all()\
            .filter(address_type='shipping').first()

    def update_address(self, geohash, lat, lng, street, pincode):
        """Update the shipping address of the order

        :param geohash:
        :param lat:
        :param lng:
        :param street:
        :return:
        """
        self.shipping_address.o_longitude = lng
        self.shipping_address.o_latitude = lat
        self.shipping_address.geohash = geohash

        if pincode:
            self.shipping_address.postcode = pincode

        street_components = self.shipping_address.street.split('\n')
        if len(street_components) < 2:
            street_components.append(street)
        else:
            street_components[1] = street

        self.shipping_address.street = '\n'.join(street_components)

        self.shipping_address.save()

        return
