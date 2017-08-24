"""All driver controller related actions."""
import logging

from app.core.models import SalesFlatOrder
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

        elif DriverOrder.objects.filter(increment_id=order):
            raise ValueError('This order is already assigned')

        else:
            driver_object = DriverOrder.objects.create(
                increment_id=order,
                driver_id=self.driver.customer.entity_id)

            with app.producer_or_acquire() as producer:
                producer.publish(
                    {"increment_id": order,
                     "status": 'out_delivery'},
                    serializer='json',
                    exchange=ORDER_STATE,
                    declare=[ORDER_STATE]
                )

            driver_object.save()
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

        logger.info(
            'The Driver {} Unassign to this order {}'.format(
                self.driver.customer.entity_id,
                order))

        with app.producer_or_acquire() as producer:
            producer.publish(
                {"increment_id": order,
                 "status": 'processing'},
                serializer='json',
                exchange=ORDER_STATE,
                declare=[ORDER_STATE]
            )

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
            status='Processing')
        return order_obj

    def complete_order(self, order_id):
        """Publish the message to the Mage queues.

        Params:
            order_id (str): Increment ID

        """
        logger.info("Complete this order {}".format(order_id))
        with app.producer_or_acquire() as producer:
            producer.publish(
                {"increment_id": order_id,
                 "status": 'complete'},
                serializer='json',
                exchange=ORDER_STATE,
                declare=[ORDER_STATE]
            )
