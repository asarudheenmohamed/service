"""Endpoint to update the all driver trip distance."""

import logging

from app.driver.lib.trip_controller import TripController
from app.driver.models.driver_order import (DriverPosition, DriverTrip,
                                            OrderEvents)

logger = logging.getLogger(__name__)


class ComputeDriverTrip:

    def __init__(self):
        pass

    def calculate_distance(self):
        """Updating the driver trip distance."""

        # fetch all trip
        driver_trip = DriverTrip.objects.all()
        logger.info('fetched the all driver trip objects')
        for trip in driver_trip:

            logger.info(
                'To update the driver trip distance for this trip:{}'.format(
                    trip.id))

            TripController().compute_driver_trip_distance(trip)

            logger.info('Trip:{} distance has been updated'.format(trip.id))
