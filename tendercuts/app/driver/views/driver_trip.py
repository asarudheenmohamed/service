"""Endpoint for  Driver Trip."""

import logging

from rest_framework import viewsets

from app.driver import serializer
from app.driver.lib.trip_controller import TripController

from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)
from app.driver.models.driver_order import *


class DriverTripViewSet(viewsets.ReadOnlyModelViewSet):
    """Returns a last 10 days driver trip."""
    authentication_classes = (DriverAuthentication,)
    serializer_class = serializer.DrivertripSerializer

    def get_queryset(self):
        """Fetch last 10 days driver trip object."""
        controller = TripController()

        logger.debug(
            "To fetch the driver trip object for the driver:{}".format(self.request.user.username))
        trip_obj = controller.fetch_driver_trip(self.request.user)

        return trip_obj
