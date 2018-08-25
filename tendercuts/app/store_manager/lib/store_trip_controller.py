"Returns  river trip obj and driver details based on store id."""
import logging
import operator

from app.core.models import SalesFlatOrder
from app.driver.models import DriverTrip


logger = logging.getLogger(__name__)


class StoreTripController(object):
    """Store order controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_trips(self, store_id):
        """Get the currently active trips.

            :params store_id(int): Store id
            returns: DriveTrip[]

        """
        increment_ids = SalesFlatOrder.objects.filter(store__store_id=int(1), status='out_delivery')
        increment_ids = increment_ids.values_list('increment_id')
        increment_ids = map(operator.itemgetter(0), increment_ids)
        
        trips = DriverTrip.objects.filter(driver_order__increment_id__in=increment_ids)

        return trips

