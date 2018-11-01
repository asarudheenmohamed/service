"""Returns assigned driver order obj and driver details based on store id."""
import datetime
import logging

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.driver.models import DriverPosition
from app.driver.models.driver_order import (DriverOrder, DriverPosition,
                                            DriverStat, DriverTrip)

logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    @classmethod
    def get_driver_obj(cls, phone_number):
        """To get driver user object.

        Params:
            phone_number(int): driver phone_number

        Returns:
            Returns driver user object.

        """
        driver_username = CustomerSearchController.get_django_username(
            phone_number)

        driver_user_obj = User.objects.get(username=driver_username)

        logger.info("fetched driver user object:{}".format(driver_user_obj))

        return driver_user_obj


    def get_driver_location(self, driver_id):
        """Fetch driver current location.

        Params:
            driver_obj(object): driver_user_obj

        Returns:
            Returns driver current latitude and longitude.

        """
        driver_position_obj = DriverPosition.objects.filter(
            driver_user_id=driver_id).last()

        return driver_position_obj

    def _update_driver_details(self,driver_user,order_ids):
        """Update driver name and driver number in sale order object.

        params:
           order_obj (obj): sale order object

        """
        user_id=driver_user.username.split(":")[1]
        driver_details = CustomerSearchController.load_cache_basic_info(
            user_id)

        SalesFlatOrder.objects.filter(
            increment_id__in=order_ids).update(
            driver_number=driver_details['phone'],
            driver_name=driver_details['name'])

        logger.info(
            'The order:{} assigned driver details like driver name:{}, and driver number:{} updated'.format(
                order_ids, driver_details['name'], driver_details['phone']))



    def store_manager_assign_orders(self, data):
        """Assign orders in driver trip.

        params:
         data (dict):{'dariver_user':1313,driver_orders:[21323,545543]}

        Returns:
            driver trip

        """
        
        active_trip = DriverTrip.objects.filter(
            driver_user_id=data.get('driver_user'),
            status=DriverTrip.Status.STARTED.value)

        if len(active_trip) >= 1:
            raise HttpResponseForbidden

        assign_order=DriverOrder.objects.filter(~Q(driver_user_id=data.get('driver_user')),
                                    increment_id__in=data.get('driver_order'))
        if assign_order:
            raise HttpResponseForbidden

        trip, status=DriverTrip.objects.get_or_create(
            driver_user_id=data.get('driver_user'),
            status=DriverTrip.Status.CREATED.value)  # type: DriverTrip

        if 'driver_order' in data:
            for order in data.get('driver_order'):
                order, status=DriverOrder.objects.get_or_create(
                    driver_user_id=data.get('driver_user'), increment_id=order)
                trip.driver_order.add(order)

            trip.auto_assigned=True
            trip.save()
        self._update_driver_details(trip.driver_user,data.get('driver_order'))

        return trip
