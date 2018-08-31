"""Endpoint to get selected store driver orders."""
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from app.store_manager.lib import StoreBaseController

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

        controller = StoreBaseController(store_id)
        driver_data = controller.get_current_drivers()

        return Response(driver_data)
