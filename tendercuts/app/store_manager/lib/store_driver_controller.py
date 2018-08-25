"Returns  river trip obj and driver details based on store id."""
import logging
import operator
import collections

from app.core.models import SalesFlatOrder, CustomerEntityVarchar
from app.driver.models import DriverOrder


logger = logging.getLogger(__name__)

class StoreDriverController(object):
    """Store order controller."""

    def get_drivers(self, store_id):
        """Get the currently active drivers.
        VERY HACKY
        TODO: Needs to be refactored once we move driver auth into django directly.

            :params store_id(int): Store id
            returns: DriveTrip[]

        """
        # Get currently active orders
        increment_ids = SalesFlatOrder.objects.filter(store__store_id=int(1), status='out_delivery')
        increment_ids = increment_ids.values_list('increment_id')
        increment_ids = map(operator.itemgetter(0), increment_ids)
        
        # Get currently active list. and create dj_id -> mg_id
        user_ids = DriverOrder.objects.filter(increment_id__in=increment_ids)
        user_ids = user_ids.values_list('driver_user_id__username', 'driver_user_id__id')
        dj_user_ids = map(operator.itemgetter(1), user_ids)
        # extract and reformat driver ids to mage ids
        mage_user_ids = map(operator.itemgetter(0), user_ids)
        mage_user_ids = [int(uid.split(":")[1]) for uid in mage_user_ids]
        user_ids = dict(zip(mage_user_ids, dj_user_ids))

        # load the basic info of the driver
        fields = CustomerEntityVarchar.objects.filter(
            attribute_id__in=[149, 5], entity_id__in=list(user_ids.keys()))

        data = collections.defaultdict(dict)

        attr_map = {149: 'phone', 5: 'name'}
        for attr in fields:
            attr_name = attr_map[attr.attribute_id]
            
            data[attr.entity_id][attr_name] = attr.value
            data[attr.entity_id]['driver_user'] = user_ids[attr.entity_id]

        return list(data.values())

