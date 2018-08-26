"""Endpoint to get selected store driver orders."""
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.order_controller import OrderController
import app.core.lib.magento as mage
from app.core.models import SalesFlatOrder

from ..auth import StoreManagerAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OrderProcessingView(APIView):
    """Endpoint to get all active trip objects.

    EndPoint:
        API: store_manager/processing/

    """

    authentication_classes = (StoreManagerAuthentication,)

    def get(self, request):
        """Get all active state trip objects.

        Input:
            store_id

        returns:
            return store_data(DriverTrip Object)

        """
        orders = request.GET['orders']
        conn = mage.Connector()

        orders = SalesFlatOrder.objects.filter(increment_id__in=orders)
        for order in orders:
            controller = OrderController(conn, order)
            controller.processing()

        return Response({'status': True})
