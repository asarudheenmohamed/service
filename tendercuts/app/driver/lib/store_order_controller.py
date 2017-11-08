"""Returns assigned driver order obj and driver details based on store id."""
import logging
from datetime import date
from itertools import groupby

from django.conf import settings
from django.db.models import Max

from app.core.lib import cache
from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.core.models.customer import CustomerEntityVarchar

from ..models import DriverOrder, DriverPosition, OrderEvents

logger = logging.getLogger(__name__)


class StoreOrderController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_complete_order_ids(self, driver_ids):
        """Return current date driver's completed order ids dict objects.

        Args:
         driver_ids(list): driver entity_ids

        """
        order_event_objs = OrderEvents.objects.filter(
            driver__driver_id__in=driver_ids,
            status='completed',
            updated_time__gte=date.today()).prefetch_related('driver')

        logger.info(
            "Fetch driver's current date completed orders for that driver ids:{}".format(list(driver_ids)))
        # the query set object convert to custom dict object
        driver_complete_orders = {}
        for driver_id, objects in groupby(
                order_event_objs, lambda order_event_obj: order_event_obj.driver.driver_id):
            complete_order_ids = []
            for obj in objects:
                complete_order_ids.append(obj.driver.increment_id)
            driver_complete_orders[driver_id] = complete_order_ids

        return driver_complete_orders

    def get_lat_and_lon(self, driver_ids):
        """Return a current lat and lon driver position dict object.

        Params:
          driver_ids(list): driver entity ids

        """
        driver_lat_and_lon_records = DriverPosition.objects.values('driver_id', 'latitude', 'longitude').annotate(
            recorded_time=Max('recorded_time')).filter(
            driver_id__in=driver_ids)

        logger.info(
            "Fetch driver's current positions for that driver ids:{}".format(list(driver_ids)))

        # the query set object convert to custom dict object
        driver_lat_lon = {}
        for driver_lat_lon_obj in driver_lat_and_lon_records:
            driver_lat_lon[driver_lat_lon_obj[
                'driver_id']] = driver_lat_lon_obj

        return driver_lat_lon

    def driver_load_basic_info(self, driver_ids):
        """Fetch the driver basic info and stored in django cache.

        Args:
         driver_ids(list):driver entity ids

        Returns:
            A dict of (userid, email, phone, name)

        """
        query_set = CustomerEntityVarchar.objects                 \
            .filter(attribute_id__in=[149, 5], entity_id__in=driver_ids) \
            .order_by('-attribute_id')                             \
            .values_list('entity', 'entity__email', 'value')
        # the query set object convert to custom dict object
        driver_info = {}
        for driver_obj in query_set:
            if driver_obj[0] not in driver_info:
                driver_details = {
                    'entity_id': driver_obj[0],
                    'email': driver_obj[1],
                    'phone': driver_obj[2]
                }
                driver_info[
                    driver_obj[0]] = driver_details
                # set driver basic information in django cache
                logger.debug(
                    "Set driver's phone,entity_id and email in django cache:{}".format(
                        driver_id))

                cache.set_key(driver_obj[0], driver_details, 60 * 60 *
                              24, settings.CACHE_DEFAULT_VERSION)
            else:
                driver_details = driver_info.get(driver_obj[0])
                driver_details['name'] = driver_obj[2]
                # set driver basic information in django cache
                logger.debug(
                    "Set driver username in django cache:{}".format(
                        driver_id))

                cache.set_key(driver_obj[0], driver_details, 60 * 60 *
                              24, settings.CACHE_DEFAULT_VERSION)

        logger.info(
            "Fetch driver's information from the CustomerEntityVarchar models and set the values in django cache for that driver ids:{}".format(
                list(driver_ids)))

        return driver_info

    def get_driver_basic_info(self, driver_ids):
        """Return a driver basic information.

        Params:
            driver_ids(list): driver entity_id's
        """
        cache_no_ids = []
        driver_info = {}
        for driver_id in driver_ids:
            # get driver basic info in django cache
            logger.debug(
                'get driver information in django cache for that driver ids:{}'.format(
                    driver_ids))

            cache_driver_details = cache.get_key(
                driver_id, settings.CACHE_DEFAULT_VERSION)
            if not cache_driver_details:
                cache_no_ids.append(driver_id)
            else:
                driver_info[driver_id] = cache_driver_details
        if cache_no_ids:
            # fetch drive information from CustomerEntityVarchar model.
            logger.debug(
                "fetch driver's information in CustomerEntityVarchar model:{}".format(
                    driver_id))

            load_info_cache_no_ids = self.driver_load_basic_info(cache_no_ids)
            driver_info.update(load_info_cache_no_ids)

        logger.info(
            "get driver's information for the given driver ids:{}".format(
                list(driver_ids)))

        return driver_info

    def get_driver_orders(self, sale_order_ids):
        """Fetch driver ids based on out_delivery orders increment ids.

        Params(list): sale order increment ids

        """
        driver_objs = DriverOrder.objects.filter(
            increment_id__in=list(sale_order_ids))
        # the query set objects converts to custom dict object
        driver_orders = {}
        for driver_id, objects in groupby(
                driver_objs, lambda driver_obj: driver_obj.driver_id):
            order_ids = []
            for obj in objects:
                order_ids.append(obj.increment_id)
            driver_orders[driver_id] = order_ids

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
        sales_order_ids = SalesFlatOrder.objects.filter(
            store__store_id=int(store_id), status='out_delivery').values_list(
            'increment_id', flat=True)
        # get driver current assigning orders
        driver_orders = self.get_driver_orders(sales_order_ids)
        driver_ids = list(driver_orders.keys())
        # get driver current location
        driver_lat_lon = self.get_lat_and_lon(
            driver_ids)
        # fetch driver current date completed orders
        driver_complete_orders = self.get_complete_order_ids(
            driver_ids)
        # fetch diver basic info phone,mail,name
        load_basic_info = self.get_driver_basic_info(
            driver_ids)

        driver_objects = []
        for driver_id in driver_ids:
            driver_obj = {}
            driver_obj['lat_and_lon'] = driver_lat_lon.get(int(driver_id))
            driver_obj['complete_orders'] = driver_complete_orders.get(
                driver_id)
            driver_basic_info = load_basic_info.get(int(driver_id))
            driver_obj.update(driver_basic_info)
            driver_obj['orders'] = driver_orders.get(driver_id)
            driver_objects.append(driver_obj)

        logger.info(
            'Fetched the all Driver events object and driver details in that store:{}'.format(
                store_id))

        data = {
            'driver_objects': driver_objects,
            'select_store': {'id': int(store_id)}}

        return data
