"""All driver controller related actions."""

import logging

import app.core.lib.magento as mage
from app.core.lib.communication import SMS
from app.core.lib.order_controller import OrderController
from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.driver import tasks

from ..models import DriverOrder, DriverPosition, DriverStat, OrderEvents

logger = logging.getLogger(__name__)


class DriverController(object):
    """Driver controller."""

    def __init__(self, driver):
        """Constructor."""
        super(DriverController, self).__init__()
        self.driver = driver
        self.conn = mage.Connector()

    @classmethod
    def driver_obj(cls, user_id):
        """Fetch Flatcustomer object by using user_id."""
        driver = CustomerSearchController.load_by_id(user_id)
        return cls(driver)

    def get_order_obj(self, order):
        """Get order object based on order id.

        Params:
            order: (str) increment_id

        """
        order_obj = SalesFlatOrder.objects.filter(increment_id=order)
        if not order_obj:
            raise ValueError('Order object Does not exist')

        return order_obj[0]

    def assign_order(self, order, store_id, lat, lon):
        """Assign the order to the driver.

        Also publishes the order status to the queue.

        Params:
            order: (SalesFlatOrder|str) Order obj or increment_id
            store_id (str): store id
            lat(int): Driver location latitude
            lon(lon): Driver location longitude

        Returns:
            obj DriverOrder

        """
        order_obj = self.get_order_obj(order)

        if int(store_id) != order_obj.store_id:
            raise ValueError('Store mismatch')

        elif DriverOrder.objects.filter(increment_id=order_obj.increment_id):
            raise ValueError('This order is already assigned')

        driver_object = DriverOrder.objects.create(
            increment_id=order, driver_id=self.driver.entity_id)

        logger.info(
            '{} this order assigned to the driver {}'.format(
                order, self.driver.entity_id))

        controller = OrderController(self.conn, order_obj)
        # the order move to out for delivery
        logger.info(
            'This order:{} move to out for delivery.'.format(order))

        controller.out_delivery()
        # update current location for driver
        position_obj = self.record_position(lat, lon)

        self._record_events(driver_object, position_obj, 'out_delivery')

        tasks.send_sms.delay(order)
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
            'The Driver {} unassigned to this order {}'.format(
                self.driver.entity_id,
                order))

    def fetch_orders(self, status):
        """Return all active orders.

        Returns
            [SalesFlatOrder]

        """
        order_ids = DriverOrder.objects.filter(
            driver_id=self.driver.entity_id) \
            .values_list('increment_id', flat=True)

        logger.info(
            'Fetch that {} Driver assigning {} state orders'.format(
                self.driver.entity_id, status))

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

    def complete_order(self, order_id, lat, lon):
        """Publish the message to the Mage queues.

        Params:
            order_id (str): Increment ID
            lat(int): Driver location latitude
            lon(lon): Driver location longitude

        """
        logger.info("Complete this order {}".format(order_id))

        order_obj = self.get_order_obj(order_id)
        driver_object = DriverOrder.objects.filter(
            increment_id=order_id, driver_id=self.driver.entity_id)
        controller = OrderController(self.conn, order_obj)
        controller.complete()
        # send sms to customer
        tasks.send_sms.delay(order_id)

        # update current location for driver
        position_obj = self.record_position(lat, lon)
        self._record_events(driver_object[0], position_obj, 'completed')

    def record_position(self, lat, lon):
        """Create a Driver current location latitude and longitude.

        Params:
            order_id: order increment id
            lat(int): driver location latitude
            lon(int): driver location longitude

        Returns:
            Returns DriverPosition object

        """
        obj = DriverPosition(
            driver_id=self.driver.entity_id, latitude=lat, longitude=lon)
        obj.save()
        logger.info(
            "update the location, latitude and longitude for that driver {}".format(
                obj.driver_id))

        return obj

    def _record_events(self, driver_object, driver_position, status):
        """Create a Driver current locations.

        Params:

            locations(str):driver current locations
            status(str): order status

        Returns:
            Returns OrderEvents object

        """
        events_obj = OrderEvents.objects.create(
            driver=driver_object,
            driver_position=driver_position,
            status=status)
        logger.info(
            "update the location and order status for that driver {}".format(
                events_obj.driver_position.driver_id))

        return events_obj

    def driver_delay_sms(self, order_id):
        """Send SMS to the customer.

        Params:
            order_id(str):Customer placed order_id

        Returns:
            Returns True

        """
        customer_id = self.get_order_obj(order_id).customer_id
        customer = CustomerSearchController.load_basic_info(customer_id)
        SMS().send(customer[2], 'I am in traffic, Sorry for the delay')
        status = True

        logger.info(
            "sending the delay SMS to the customer:{}".format(
                customer[0]))

        return status

    def driver_stat_orders(self):
        """Returns a driver stat object."""
        driver_stat_obj = DriverStat.objects.filter(
            driver_id=self.driver.entity_id)

        return driver_stat_obj
