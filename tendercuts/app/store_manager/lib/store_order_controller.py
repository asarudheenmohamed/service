"""Returns assigned driver order obj and driver details based on store id."""
import logging
import datetime

from django.contrib.auth.models import User
from django.db.models import Q


from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.driver.models import DriverPosition

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
