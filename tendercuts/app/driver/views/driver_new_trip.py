"""Endpoint for new Driver Trip."""

import logging

from rest_framework import viewsets, decorators
from rest_framework.response import Response

from app.driver import serializer
from app.driver.lib.new_trip_controller import DriverTripController
from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class NewDriverTripViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides teh following apis
    /driver/trip -> get all completed trips
    /driver/trip/current/ -> get or create a current/new trip
    /driver/trip/current/start -> begin trip.

    """
    authentication_classes = (DriverAuthentication,)
    serializer_class = serializer.DrivertripSerializer

    def get_queryset(self):
        """Override to retrieve the current driver's trip"""
        trips = DriverTripController.get_completed_trips(
            self.request.user)

        return trips

    def get_object(self):
        """Override to get or create a new trip"""
        trip = DriverTripController.get_or_create_trip(self.request.user)

        return trip

    @decorators.detail_route(methods=['get'])
    def start(self, *args, **kwargs):
        trip = self.get_object()
        DriverTripController(trip=trip).start_trip()

        return Response({'status': True})

    @decorators.detail_route(methods=['get'])
    def pending_orders(self, *args, **kwargs):
        trip = self.get_object()
        controller = DriverTripController(trip=trip)

        return Response({'status': True})

    @decorators.detail_route(methods=['get'])
    def get_current_trip(self, *args, **kwargs):
        """Get or generate a driver trip."""
        trip = self.get_object()

        return trip
