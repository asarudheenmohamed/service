"""Returns assigned driver order obj and driver details based on store id."""
import logging

from app.core.models import SalesFlatOrder

logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    def store_orders(self, store_id):
        """Fetch active state order objects.

        Params:
            store_id(int): store id
        Returns:
            Returns all active order obj.

        """
        sales_order_obj = SalesFlatOrder.objects.filter(
            store__store_id=int(store_id)).exclude(status__in=['canceled','complete','closed'])

        logger.info(
            "fetched 'out_delivery' and 'complete' state order obj in store:{}".format(
                store_id))

        return sales_order_obj
