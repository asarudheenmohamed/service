"""Returns assigned driver order obj and driver details based on store id."""
import logging

from app.core.lib.user_controller import CustomerSearchController
from app.core.models.customer.entity import CustomerEntity
from app.driver.constants import DRIVER_GROUP

from ..models import DriverOrder, DriverPosition, OrderEvents

logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_order_ids(self, driver_id):
        """Fetch current driver assigned order ids.

        Args:
         driver_id(int): driver entity_id

        """
        orders = [
            order_event_obj.driver_position.driver.increment_id for order_event_obj in OrderEvents.objects.filter(
                driver_position__driver__driver_id=driver_id,
                status='out_delivery')]

        return orders

    def get_store_driver_order(self, store_id):
        """Fetch drivers assigned order objects in that store.

        Params:
            store_id(int): store id
        Returns:
            Returns assigned driver order obj and driver details based on store id.

        """

        driver_entity_obj = CustomerEntity.objects.filter(
            store__store_id=int(store_id), group_id=DRIVER_GROUP)

        logger.info(
            'fetched the driver object in store id:{}'.format(store_id))
        print 'asssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'
        driver_position_obj = [DriverPosition.objects.filter(driver__driver_id=driver_obj.entity_id).order_by('-recorded_time')[0]
                               for driver_obj in driver_entity_obj if DriverOrder.objects.filter(driver_id=driver_obj.entity_id)]
        order_event_obj = [OrderEvents.objects.filter(driver_position=obj).order_by(
            '-updated_time')[0] for obj in driver_position_obj if OrderEvents.objects.filter(driver_position=obj)]

        driver_objects = map(lambda x, y: {'obj': y, 'entity_id': x[0], 'phone': x[2], 'email': x[1], 'orders': self.get_order_ids(x[0]), 'name': x[3]}, map(lambda x: CustomerSearchController.load_basic_info(
            x.driver_position.driver.driver_id), order_event_obj), order_event_obj)

        logger.info(
            'Fetched the all Driver events object and driver details in that store:{}'.format(store_id))

        data = {
            'driver_objects': driver_objects,
            'select_store': {'id': int(store_id)}}

        return data
