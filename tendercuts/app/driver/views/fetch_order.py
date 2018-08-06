"""Endpoint for the sales flat order object."""

import logging

from rest_framework import viewsets

from app.core import serializers
from app.core.lib.utils import get_user_id
from app.core.lib.user_controller import CustomerSearchController


from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FetchRelatedOrder(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Endpoint to provide a list for sales orders object

    """
    authentication_classes = (DriverAuthentication,)
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        """Return a query set containing sale order of the driver."""
        order_end_id = self.request.GET.get('order_id')
        store_id = self.request.GET.get('store_id')
        user_id = get_user_id(self.request)
        driver = CustomerSearchController.load_by_id(user_id)

        logger.info(
            "Fetch related order for the store id:{} with order id's last digits {}".format(store_id, order_end_id))

        controller = DriverController(driver)
        order_obj = controller.fetch_related_orders(order_end_id, store_id)

        return order_obj
