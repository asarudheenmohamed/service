"""All driver controller related actions."""

import logging

from django.conf import settings
from django.utils import timezone

import app.core.lib.magento as mage
import geopy.distance
from app.core.lib.communication import SMS
from app.core.lib.order_controller import OrderController
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_mage_userid
from app.core.models import SalesFlatOrder
from app.core.models.customer.address import CustomerAddressEntity
from app.driver import tasks

from ..models import (DriverOrder, DriverPosition, DriverStat, DriverTrip,
                      OrderEvents)
from .trip_controller import TripController

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

    def update_driver_details(self, order_obj):
        """Update driver name and driver number in sale order object.

        params:
           order_obj (obj): sale order object

        """
        user_id = get_mage_userid(self.driver)
        # fetch driver basic info
        driver_details = CustomerSearchController.load_cache_basic_info(
            user_id)
        order_obj.driver_number = driver_details['phone']
        order_obj.driver_name = driver_details['name']

        order_obj.save()

        logger.info(
            'The order:{} assigned driver details like driver name:{}, and driver number:{} updated'.format(
                order_obj.increment_id, driver_details['name'], driver_details['phone']))

    def get_order_obj(self, order):
        """Get order object based on order id.

        Params:
            order: (str) increment_id

        """
        order_obj = SalesFlatOrder.objects.filter(increment_id=order)
        if not order_obj:
            raise ValueError('Order object Does not exist')

        return order_obj[0]

    def _get_distance(self, lat, lng, dest_lat, dest_lng):
        """Compute crow flying distance between customer location and driver completed location.

        :param warhouse_id: (stock.warehouse)
        :param lat: (float)
        :param lng: (float)

        :return: (float) distance
        """
        return geopy.distance.vincenty((dest_lat, dest_lng), (lat, lng)).km

    def is_nearby(self, order, latitude, longitude):
        """Check the driver completed location is inside the customer geolocation radius.500m

        Params:
            order(obj): order object
            latitude: driver completed location latitude
            longitude: driver completed location longitude
        """
        shipping_address = order.shipping_address.all().first()
        if not shipping_address.geohash:
            return False

        return self._get_distance(
            latitude, longitude, shipping_address.o_latitude, shipping_address.o_longitude) < 0.5

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
        order_obj = SalesFlatOrder.objects.filter(
            increment_id=order, status='processing')
        if not order_obj:
            raise ValueError('Order object Does not exist')

        order_obj = order_obj[0]
        logger.debug(
            'Fetched the order object of given order id:{}'.format(order))

        if int(store_id) != order_obj.store_id:
            raise ValueError('Store mismatch')

        elif DriverOrder.objects.filter(increment_id=order_obj.increment_id):
            raise ValueError('This order is already assigned')

        try:
            lat, lon = settings.STORE_LAT_LONG[int(store_id)]
        except KeyError:
            pass

        driver_object = DriverOrder.objects.create(
            increment_id=order, driver_user=self.driver)

        # update driver name and driver number in sale order object
        self.update_driver_details(order_obj)

        logger.info(
            'The order:{} was assigned to the driver {}'.format(
                order, self.driver.username))

        controller = OrderController(self.conn, order_obj)
        # the order move to out for delivery
        logger.info(
            'This order:{} will move to out for delivery.'.format(order))

        controller.out_delivery()
        # update current location for driver
        position_obj = self.record_position(lat, lon)

        logger.debug(
            "updated the assigned order:{}'s lat:{} and lon:{} for the driver".format(
                self.driver.username, lat, lon))

        self._record_events(driver_object, position_obj, 'out_delivery')

        TripController(
            driver=self.driver).check_and_create_trip(
            driver_object, position_obj)

        tasks.send_sms.delay(order, 'out_delivery')

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
                self.driver.username,
                order))

    def fetch_orders(self, status):
        """Return all active orders.

        Returns
            [SalesFlatOrder]

        """
        order_ids = DriverOrder.objects.filter(
            driver_user=self.driver,
            created_at__startswith=timezone.now().date()).order_by('created_at').values_list(
            'increment_id',
            flat=True)

        order_obj = SalesFlatOrder.objects.filter(
            increment_id__in=list(order_ids),
            status=status)[:10]
        logger.debug(
            'Fetched the SalesFlatOrder objects for the list of order ids:{} '.format(
                order_ids))

        return order_obj

    def fetch_related_orders(self, order_end_id, store_id):
        """Return Sales Order objects.

        Params:
         order_end_id(str): order last 4 digit number
         store id(str): store id

        Returns:
            [SalesFlatOrder]

        """

        order_obj = SalesFlatOrder.objects.filter(
            increment_id__endswith=order_end_id,
            store_id=store_id,
            status='processing')

        logger.debug(
            "Fetched the related orders for the store id:{} with order last digits".format(
                store_id, order_end_id))

        return order_obj

    def update_order_completed_location(self, order_obj, lat, lon):
        """Update order completed location like lat and lon.
        params:
         order_obj (obj):sale order object
         lat (str):geolocation latitude
         lon (lon):geolocation longitude

        """
        order_obj.shipping_address.all().update(
            latitude=lat, longitude=lon)

    def complete_order(self, order_id, lat, lon):
        """Publish the message to the Mage queues.

        Params:
            order_id (str): Increment ID
            lat(int): Driver location latitude
            lon(lon): Driver location longitude

        """
        logger.info("Complete this order {}".format(order_id))
        order_obj = self.get_order_obj(order_id)

        # checks the driver completed location with in a customer geolocation
        # radius 500m
        if not is_nearby(order_obj, lat, lon):
            logger.info(
                "This driver:{} is trying to complete the order ahead of customer location".format(
                    self.driver.username))

            raise ValueError(
                'Please Complete the order customer nearest locations')

        driver_object = DriverOrder.objects.filter(
            increment_id=order_id, driver_user=self.driver)
        controller = OrderController(self.conn, order_obj)
        controller.complete()
        # update customer current location
        position_obj = self.update_order_completed_location(
            order_obj, lat, lon)

        # ToDo commended a customer current location updated because location is not correct
        #tasks.customer_current_location.delay(order_obj.customer_id, lat, lon)

        # send sms to customer
        tasks.send_sms.delay(order_id, 'complete')
        tasks.driver_stat.delay(order_id)

        # update current location for driver
        position_obj = self.record_position(lat, lon)
        self._record_events(driver_object[0], position_obj, 'completed')

        try:
            TripController(driver=self.driver).check_and_complete_trip(
                driver_object[0], position_obj)
        except ValueError:
            # Legacy handling
            pass

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
            driver_user=self.driver,
            latitude=lat,
            longitude=lon)
        obj.save()
        logger.info(
            "updated driver:{}'s current latitude:{} and longitude:{}".format(
                obj.driver_id, lat, lon))

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
            "updated the order events of the driver {}".format(
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
            driver_user=self.driver)
        logger.info(
            'Fetched the driver stat object for the driver:{}'.format(
                self.driver))

        return driver_stat_obj
