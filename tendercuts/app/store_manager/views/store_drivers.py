"""Endpoint to get selected store driver orders."""
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from app.store_manager.lib import StoreDriverController

from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreDriverView(APIView):
    """Endpoint to get all active trip objects.

    EndPoint:
        API: store_manager/trips/

    """

    authentication_classes = (StoreManagerAuthentication,)

    def get(self, request):
        """Get all active state trip objects.

        Input:
            store_id

        returns:
            return store_data(DriverTrip Object)

        """
        store_id = request.GET['store_id']

        controller = StoreDriverController()
        driver_data = controller.get_drivers(store_id)

        return Response(driver_data)
