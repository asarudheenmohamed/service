"""Returns  driver trip obj and driver details based on store id."""
import logging
import operator
import datetime
import collections

from app.core.models import SalesFlatOrder, CustomerEntityVarchar
from app.driver.models import DriverTrip, DriverOrder, DriverLoginLogout


logger = logging.getLogger(__name__)


class StoreBaseController(object):
    """Store order controller."""

    def __init__(self, store_id):
        self.store_id = store_id

    @property
    def today(self):
        # return format(datetime.date.today(), '%Y-%m-%d')
        return format(datetime.date.today(), '%Y-%m-%d')

    def get_current_orders(self, status):
        """Get the current orders in store"""
        orders = SalesFlatOrder.objects.filter(
            store__store_id=int(self.store_id),
            status__in=status,
            sale_date__gt=self.today,
            sale_date__lte="{} 23:59:59".format(self.today),
        )

        return orders

    def get_current_trips(self):
        """Get the currently active trips.

            :params store_id(int): Store id
            returns: DriveTrip[]

        """
        increment_ids = self.get_current_orders(status=['out_delivery'])
        increment_ids = increment_ids.values_list('increment_id')
        increment_ids = map(operator.itemgetter(0), increment_ids)

        trips = DriverTrip.objects.filter(
            driver_order__increment_id__in=increment_ids)

        return trips

    def get_current_drivers(self):
        """Get the currently active drivers.
           VERY HACKY
        TODO: Needs to be refactored once we move driver auth into django directly.

        :params store_id(int): Store id
        returns: DriveTrip[]

        """
        # tuple of mage_id, dj_id
        driver_objs = DriverLoginLogout.objects.filter(
            store_id=self.store_id).values_list(
            'driver__username', 'driver_id')
        
        user_ids = {}
        for mage_id, dj_id in driver_objs:
            entity_id = mage_id.split(":")[1]
            user_ids[int(entity_id)] = dj_id

        # load the basic info of the driver
        fields = CustomerEntityVarchar.objects.filter(
            attribute_id__in=[149, 5], entity_id__in=user_ids.keys())

        data = collections.defaultdict(dict)

        attr_map = {149: 'phone', 5: 'name'}
        for attr in fields:
            attr_name = attr_map[attr.attribute_id]

            data[attr.entity_id][attr_name] = attr.value
            data[attr.entity_id]['driver_user'] = attr.entity_id
            data[attr.entity_id]['id'] = user_ids[attr.entity_id]

        return list(data.values())
