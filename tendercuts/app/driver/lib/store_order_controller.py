"""Returns assigned driver order obj and driver details based on store id."""
import logging
from datetime import date

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder

from ..models import DriverOrder, DriverPosition, OrderEvents

logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_order_ids(self, driver_id, order_ids):
        """Fetch current driver assigned order ids.

        Args:
         driver_id(int): driver entity_id

        """
        orders = [order_id[0] for order_id in order_ids if OrderEvents.objects.filter(
            driver_position__driver__driver_id=driver_id,
            driver_position__driver__increment_id=order_id[0]).order_by('-updated_time') and OrderEvents.objects.filter(
            driver_position__driver__driver_id=driver_id,
            driver_position__driver__increment_id=order_id[0]).order_by('-updated_time')[0].status
            == 'out_delivery']

        return orders

    def get_complete_order_ids(self, driver_id):
        """Fetch current driver assigned order ids.

        Args:
         driver_id(int): driver entity_id

        """
        ids = []
        complet_orders = [
            ids.append(order_event_obj.driver_position.driver.increment_id) for order_event_obj in OrderEvents.objects.filter(
                driver_position__driver__driver_id=driver_id,
                status='completed', updated_time__gte=date.today()) if order_event_obj.driver_position.driver.increment_id not in ids]

        return ids

    def get_lat_and_lon(self, driver_id):
        """Return a current lat and lon driver position object.

        Params:
          driver_id(int): driver entity id

        """
        current_driver_position = DriverPosition.objects.filter(
            driver__driver_id=driver_id).order_by('-recorded_time')[0]

        return current_driver_position

    def get_store_driver_order(self, store_id):
        """Fetch drivers assigned order objects in that store.

        Params:
            store_id(int): store id
        Returns:
            Returns assigned driver order obj and driver details based on store id.

        """
        logger.info(
            'fetched the driver object in store id:{}'.format(store_id))
        sales_order_id = SalesFlatOrder.objects.filter(
            store__store_id=int(store_id), status__in=[
                'out_delivery']).values_list('increment_id')
        driver_ids = [OrderEvents.objects.filter(
            driver_position__driver__increment_id=i[0]).order_by('-updated_time')[0].driver_position.driver.driver_id for i in sales_order_id if OrderEvents.objects.filter(
            driver_position__driver__increment_id=i[0])]

        driver_objects = map(lambda x, y: {'lat_and_lon': self.get_lat_and_lon(int(y)), 'entity_id': x[0], 'phone': x[2], 'email': x[1], 'orders': self.get_order_ids(x[0], sales_order_id), 'complete_orders': self.get_complete_order_ids(x[0]), 'name': x[3]}, map(lambda x: CustomerSearchController.load_basic_info(
            int(x)), set(driver_ids)),
            set(driver_ids))

        logger.info(
            'Fetched the all Driver events object and driver details in that store:{}'.format(store_id))

        data = {
            'driver_objects': driver_objects,
            'select_store': {'id': int(store_id)}}

        return data
