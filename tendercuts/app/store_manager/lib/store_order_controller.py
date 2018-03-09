"""Returns assigned driver order obj and driver details based on store id."""
import logging
from django.contrib.auth.models import User

from app.core.models import SalesFlatOrder
from app.core.lib.user_controller import CustomerSearchController
from app.driver.models import DriverOrder, DriverPosition, OrderEvents
from app.core.lib.utils import get_django_username


logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    @classmethod
    def get_driver_obj(self, phone_number):
        """To get driver user object.

        Params:
            phone_number(int): driver phone_number
        Returns:
            Returns driver user object.

        """
        driver_username = get_django_username(phone_number)

        driver_user_obj = User.objects.get(username=driver_username)

        logger.info("fetched driver user object:{}".format(driver_user_obj))

        return driver_user_obj

    def store_orders(self, store_id):
        """Fetch active state order objects.

        Params:
            store_id(int): store id
        Returns:
            Returns all active order obj.

        """
        sales_order_obj = SalesFlatOrder.objects.filter(
            store__store_id=int(store_id)).exclude(status__in=['canceled', 'complete', 'closed'])

        logger.info(
            "fetched 'out_delivery' and 'complete' state order obj in store:{}".format(
                store_id))

        return sales_order_obj

    def get_driver_location(self, driver_obj):
        """Fetch driver current location.
        
        Params:
            driver_obj(object): driver_user_obj
        Returns:
            Returns driver current latitude and longitude.

        """
        driver_position_obj = DriverPosition.objects.filter(
            driver_user=driver_obj).last()

        logger.info(
            "Fetch driver's current positions for that driver ids:{}".format(
                driver_obj))

        return driver_position_obj

