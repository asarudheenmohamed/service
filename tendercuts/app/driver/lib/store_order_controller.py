"""Returns assigned driver order obj and driver details based on store id."""
import logging
from datetime import date
import itertools

from django.conf import settings
from django.db.models import Max

from app.core.lib import cache
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_mage_userid
from app.core.models import SalesFlatOrder
from app.core.models.customer import CustomerEntityVarchar

from ..models import DriverOrder, DriverPosition, OrderEvents

logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_complete_order_ids(self, driver_user):
        """Return current date driver's completed order ids dict objects.

        Args:
         driver_user(list): driver entity_ids

        """
        order_event_objs = OrderEvents.objects.filter(
            driver_order__driver_user__in=driver_user,
            status='completed',
            updated_time__gte=date.today()).prefetch_related('driver_order')

        logger.info(
            "Fetch driver's current date completed orders for that driver ids:{}".format(list(driver_user)))
        # the query set object convert to custom dict object
        driver_complete_orders = {}
        for driver_user, objects in itertools.groupby(
                order_event_objs, lambda order_event_obj: order_event_obj.driver_order.driver_id):
            complete_order_ids = []
            for obj in objects:
                complete_order_ids.append(obj.driver_order.increment_id)
            driver_complete_orders[driver_user] = complete_order_ids

        return driver_complete_orders

    def get_lat_and_lon(self, driver_user):
        """Return a current lat and lon driver position dict object.

        Params:
          driver_user(list): driver entity ids

        """
        driver_position_objs = DriverPosition.objects.values(
            'driver_user').annotate(recorded_time=Max('recorded_time'), id=Max('id')).filter(driver_user__in=list(driver_user))

        driver_lat_and_lon_records = DriverPosition.objects.filter(
            id__in=[driver_pk_id['id'] for driver_pk_id in driver_position_objs])

        logger.info(
            "Fetch driver's current positions for that driver ids:{}".format(list(driver_user)))

        # the query set object convert to custom dict object
        driver_lat_lon = {}
        for driver_lat_lon_obj in driver_lat_and_lon_records:
            driver_lat_lon[driver_lat_lon_obj.driver_user] = driver_lat_lon_obj

        return driver_lat_lon

    def get_driver_orders(self, sale_order_ids):
        """Fetch driver ids based on out_delivery orders increment ids.

        Params(list): sale order increment ids

        """
        driver_objs = DriverOrder.objects.filter(
            increment_id__in=list(sale_order_ids))
        # the query set objects converts to custom dict object
        driver_orders = {}
        for driver_user, objects in itertools.groupby(
                driver_objs, lambda driver_obj: driver_obj.driver_user):
            order_ids = []
            for obj in objects:
                order_ids.append(obj.increment_id)
            driver_orders[driver_user] = order_ids

        logger.info(
            'Fetched the driver ids for the given order ids :{}'.format(
                list(sale_order_ids)))

        return driver_orders

    def get_store_driver_order(self, store_id):
        """Fetch drivers assigned order objects in that store.

        Params:
            store_id(int): store id
        Returns:
            Returns assigned driver order obj and driver details based on store id.

        """
        logger.info(
            'fetched the driver object in store id:{}'.format(
                store_id))
        sales_order_ids = SalesFlatOrder.objects \
            .filter(store__store_id=int(store_id), status='out_delivery') \
            .values_list('increment_id', flat=True)
        # get driver's current assigning orders
        driver_orders = self.get_driver_orders(sales_order_ids)
        driver_user_objs = list(driver_orders.keys())
        # get driver's current location
        driver_lat_lon = self.get_lat_and_lon(driver_user_objs)

        # fetch driver's current date completed orders
        driver_complete_orders = self.get_complete_order_ids(
            driver_user_objs)
        # fetch diver's basic info phone,mail,name
        load_basic_info = {}
        for driver_user in driver_user_objs:
            driver_id = get_mage_userid(driver_user)
            driver_basic_info = CustomerSearchController.load_cache_basic_info(
                driver_id)
            load_basic_info[driver_user] = driver_basic_info

        driver_objects = []
        for driver_user in driver_user_objs:
            driver_obj = {}
            driver_obj['lat_and_lon'] = driver_lat_lon.get(driver_user)
            driver_obj['complete_orders'] = driver_complete_orders.get(
                driver_user)
            driver_basic_info = load_basic_info.get(driver_user)
            driver_obj.update(driver_basic_info)
            driver_obj['orders'] = driver_orders.get(driver_user)
            driver_objects.append(driver_obj)

        logger.info(
            'Fetched the all Driver events object and driver details in that store:{}'
            .format(store_id))
        data = {
            'driver_objects': driver_objects,
            'select_store': {'id': int(store_id)}}

        return data
