"""All driver online controller related actions."""

import datetime
import logging

from django.utils import timezone
from typing import Optional, Any

from ..models import DriverLoginLogout

logger = logging.getLogger(__name__)


class DriverOnlineController(object):
    """Driver online controller."""

    def __init__(self, driver):
        """Constructor."""
        super(DriverOnlineController, self).__init__()
        self.driver = driver

    def driver_checkin(self, store_id):
        """Create driver check_in object.

        Returns:
            Returns True

        """
        DriverLoginLogout.objects.create(
            driver_id=self.driver.id, store_id=store_id)

        logger.info("Created Check In detail for the driver :{},{}".format(
            self.driver,store_id))

        return True

    def driver_checkout(self):
        """Update driver check_out time..

        Returns:
            Returns True

        """
        obj = DriverLoginLogout.objects.filter(
            driver=self.driver.id,
            date=datetime.date.today(),
            check_out__isnull=True)

        logger.debug("Check whether driver: {} Checked In or not".format(
            self.driver))

        if obj:
            obj.update(check_out=datetime.datetime.now().time())
        else:
            raise ValueError("Driver didn't Check In")

        logger.info("Update check_out time for the driver :{}".format(
            self.driver))

        return True

    def driver_status(self):
        """Check driver online status.

        Returns:
            Returns True

        """
        obj = DriverLoginLogout.objects.filter(
            driver=self.driver.id,
            date=datetime.date.today(),
            check_out__isnull=True).last()  # type: DriverLoginLogout

        logger.debug("Set driver: {} online status".format(self.driver))

        if obj:
            status = (True, obj.store_id)
        else:
            status = (False, None)

        logger.info("Checked online status for the driver :{}".format(
            self.driver))

        return status
