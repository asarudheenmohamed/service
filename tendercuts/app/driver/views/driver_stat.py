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
        user_id = get_user_id(self.request)

        controller = DriverController.driver_obj(user_id)
        obj = controller.driver_stat_orders()

        return obj
