"""Endpoint for  Driver Stat."""

import logging

from rest_framework import viewsets

from app.core.lib.utils import get_user_id
from app.driver import serializer
from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverStatViewSet(viewsets.ReadOnlyModelViewSet):
    """Returns a Driver's no of completed orders."""
    authentication_classes = (DriverAuthentication,)
    serializer_class = serializer.DriverStatSerializer

    def get_queryset(self):
        """Fetch driver stat object."""

        controller = DriverController(self.request.user)

        logger.debug(
            "To fetch the driver stat object for the driver:{}".format(self.request.user.username))
        obj = controller.driver_stat_orders()

        return obj
