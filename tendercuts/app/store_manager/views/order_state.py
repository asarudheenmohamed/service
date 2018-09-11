"""Endpoint to get selected store driver orders."""
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.order_controller import OrdersController
import app.core.lib.magento as mage
from app.core.models import SalesFlatOrder

from ..auth import StoreManagerPermission

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OrderProcessingView(APIView):
    """Endpoint to get all active trip objects.

    EndPoint:
        API: store_manager/processing/

    """

    permission_classes = (StoreManagerPermission,)

    def post(self, request):
        """Get all active state trip objects.

        Input:
            store_id

        returns:
            return store_data(DriverTrip Object)

        """
        orders = request.data['orders']
        conn = mage.Connector()

        logger.info(orders)
        controller = OrdersController(conn)
        orders = SalesFlatOrder.objects.filter(increment_id__in=orders)

        filtered_orders = []
        for order in orders:
            if order.status in ['pending', 'scheduled_order']:
                filtered_orders.append(order)
        logger.info(filtered_orders)

        if filtered_orders:
            controller.processing(filtered_orders)

        return Response({'status': True})
