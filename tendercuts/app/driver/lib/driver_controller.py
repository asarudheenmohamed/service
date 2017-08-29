"""All driver controller related actions."""
import logging

import app.core.lib.magento as mage
from app.core.lib.order_controller import OrderController
from app.core.models import SalesFlatOrder
from app.driver.models.driver_order import (DriverOrder, DriverPosition,
                                            OrderEvents)
from config.celery import app
from config.messaging import ORDER_STATE

from ..models import DriverOrder

logger = logging.getLogger(__name__)


class DriverController(object):
    """Driver controller."""

    def __init__(self, driver):
        """Constructor."""
        super(DriverController, self).__init__()
        self.driver = driver
        self.conn = mage.Connector()

    def get_order_obj(self, order):
        """Get order object based on order id.

        Params:
            order: (str) increment_id

        """
        order_obj = SalesFlatOrder.objects.filter(increment_id=order)
        if not order_obj:
            raise ValueError('Order object Does not exist')

        return order_obj[0]

    def assign_order(self, order, store_id):
        """Assign the order to the driver.

        Also publishes the order status to the queue.

        Params:
            order: (SalesFlatOrder|str) Order obj or increment_id

        Returns:
            obj DriverOrder

        """
        if isinstance(order, SalesFlatOrder):
            order = order.increment_id

        obj = self.get_order_obj(order)
        if int(store_id) != obj.store_id:
            raise ValueError('Store mismatch')

        elif DriverOrder.objects.filter(increment_id=obj.increment_id):
            raise ValueError('This order is already assigned')

        else:
            driver_object = DriverOrder.objects.create(
                increment_id=order, driver_id=self.driver.customer.entity_id)
            order_obj = SalesFlatOrder.objects.filter(
                increment_id=order)
            controller = OrderController(self.conn, order_obj[0])
            controller.out_delivery()

            driver_object = DriverOrder.objects.get(
                increment_id=int(order))
            logger.info(
                '{} this order assign to the driver {}'.format(
                    order, self.driver.customer.entity_id))

            return driver_object

    def unassign_order(self, order):
        """Unassign the order to the driver.

        Also publishes the order status to the queue.

        Params:
            order(str): increment_id

        """
        obj = self.get_order_obj(order)

        driver_assigned_obj = DriverOrder.objects.filter(increment_id=order)
        driver_assigned_obj.delete()

        controller = OrderController(self.conn, obj)
        controller.processing()

        logger.info(
            'The Driver {} Unassign to this order {}'.format(
                self.driver.customer.entity_id,
                order))

    def fetch_orders(self, status):
        """Return all active orders.

        Returns
            [SalesFlatOrder]

        """
        order_ids = DriverOrder.objects.filter(
            driver_id=self.driver.customer.entity_id) \
            .values_list('increment_id', flat=True)

        logger.info(
            'Fetch that {} Driver assigning {} state orders'.format(
                self.driver.customer.entity_id, status))

        return SalesFlatOrder.objects.filter(
            increment_id__in=list(order_ids),
            status=status)

    def fetch_related_orders(self, order_end_id, store_id):
        """Return Sales Order objects.

        Params:
         order_end_id(str): order last 4 digit number
         store id(str): store id

        Returns:
            [SalesFlatOrder]

        """
        logger.info(
            'Fetch related order for that order last id {} and store id {}'.format(
                order_end_id, store_id))

        order_obj = SalesFlatOrder.objects.filter(
            increment_id__endswith=order_end_id,
            store_id=store_id,
            status='processing')
        return order_obj

    def complete_order(self, order_id):
        """Publish the message to the Mage queues.

        Params:
            order_id (str): Increment ID

        """
        logger.info("Complete this order {}".format(order_id))

        order_obj = SalesFlatOrder.objects.filter(
            increment_id=order_id)
        controller = OrderController(self.conn, order_obj[0])
        controller.complete()

    def driver_position(self, lat, lon):
        """Create a Driver current latitude and longitude.

        Params:
            lat(int): driver location latitude
            lon(int): driver location longitude

        Returns:
            Returns DriverPosition object

        """
        obj = DriverPosition.objects.create(
            driver=self.driver, latitude=lat, longitude=lon)

        logger.info(
            "update the location, latitude and longitude for that driver {}".format(
                self.driver.driver_id))

        return obj

    def order_events(self, location, status):
        """Create a Driver current locations.

        Params:
            locations(str):driver current locations
            status(str): order status

        Returns:
            Returns OrderEvents object

        """
        events_obj = OrderEvents.objects.create(
            driver=self.driver,
            location=location, status=status)

        logger.info(
            "update the location and order status for that driver {}".format(
                self.driver.driver_id))

        return events_obj
