"""Endpoint to get optimum routing."""
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from app.store_manager.lib import RoutingController
from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreRoutingView(APIView):
    """Endpoint to get all best possible trips.

    EndPoint:
        API: store_manager/routing/

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

        controller = RoutingController()
        routes = controller.generate_optimal_routes(store_id)

        return Response(routes)
