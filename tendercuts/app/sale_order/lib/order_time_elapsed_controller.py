"""Order time elapsed controller."""
import datetime
import logging

import dateutil.parser
from django.contrib.auth.models import User
from django.utils import timezone

from app.core.lib.exceptions import CustomerNotFound
from app.core.models import SalesFlatOrder
from app.core.models.customer import CustomerEntityVarchar
from app.sale_order.model import OrderTimeElapsed

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OrderTimeElapsedController(object):
    """Order time elapsed controller."""

    def __init__(self, order):
        """Constructor."""
        self.order = order
        self.slots = {52: "7:00",
                      53: "9:00",
                      54: "11:00",
                      55: "17:00",
                      56: "19:00"}

    def _complute_elapsed_time(self, ending_time, starting_time):
        """Returns the elapsed time."""
        elapsed_time = round(
            ((ending_time - starting_time).total_seconds()) / 60, 0)

        return elapsed_time if elapsed_time > 0 else 0

    def fetch_driver_basic_info(self):
        """Returns to the driver entity object."""
        query_set = CustomerEntityVarchar.objects.filter(
            attribute_id=149, value=self.order.driver_number)

        if len(query_set) == 0:
            raise CustomerNotFound()

        driver = query_set[0]

        return driver

    def create_order_elapsed_obj(self):
        """Create order elapsed object."""
        order_obj = SalesFlatOrder.objects.filter(
            increment_id=self.order.increment_id).last()

        if int(order_obj.deliverytype) == 2:
            import pytz
            pending_time = dateutil.parser.parse(
                "{} {}".format(order_obj.scheduled_date, self.slots[order_obj.scheduled_slot]))
            tz = pytz.timezone('Asia/Kolkata')
            # remove any timezone
            pending_time = pending_time.replace(tzinfo=None)
            pending_time = tz.localize(pending_time, is_dst=None)
        else:
            pending_time = self.order.created_at

        elapsed_obj, status = OrderTimeElapsed.objects.get_or_create(
            increment_id=self.order.increment_id)
        elapsed_obj.deliverytype = self.order.deliverytype
        elapsed_obj.pending_time = pending_time
        elapsed_obj.created_at = timezone.now()
        elapsed_obj.save()

        logger.info("Creating order elapsed object for order id:{}".format(
            order_obj.increment_id))

    def update_processing_elapsed(self, elapsed_obj):
        """Update order processing time and elapsed time."""

        elapsed_obj.processing_time = timezone.now()
        elapsed_obj.pending_elapsed = self._complute_elapsed_time(
            timezone.now(), elapsed_obj.pending_time)

        elapsed_obj.save()

        logger.info("Update a processing time:{} and elapsed time for order id:{}".format(
            timezone.now(), self.order.increment_id))

    def update_out_delivery_elapsed(self, elapsed_obj):
        """Update order out_delivery time and elapsed time."""
        driver = self.fetch_driver_basic_info()

        elapsed_obj.driver_user = User.objects.get(
            username='u:{}'.format(driver.entity_id))
        elapsed_obj.out_delivery_time = timezone.now()
        elapsed_obj.processing_elapsed = self._complute_elapsed_time(
            timezone.now(), elapsed_obj.processing_time)

        elapsed_obj.save()

        logger.info("Update a out_delivery time:{} and elapsed time for order id:{}".format(
            timezone.now(), self.order.increment_id))

    def update_completed_elapsed(self, elapsed_obj):
        """Update order completed time and elapsed time."""
        elapsed_obj.completed_time = timezone.now()
        elapsed_obj.out_delivery_elapsed = self._complute_elapsed_time(
            timezone.now(), elapsed_obj.out_delivery_time)

        elapsed_obj.save()

        logger.info("Update a completed time:{} and elapsed time for  order id:{}".format(
            timezone.now(), self.order.increment_id))

    def remove_order_elapsed_obj(self, elapsed_obj):
        """Remove the order elapsed object."""
        elapsed_obj.delete()

    def compute_order_status_elapsed_time(self, status):
        """Update order state time and elapsed time."""

        actions_map = {'pending': self.create_order_elapsed_obj,
                       'processing': self.update_processing_elapsed,
                       'out_delivery': self.update_out_delivery_elapsed,
                       'complete': self.update_completed_elapsed,
                       'scheduled_order': self.create_order_elapsed_obj,
                       'canceled': self.remove_order_elapsed_obj,
                       'closed': self.remove_order_elapsed_obj}

        elapsed_obj = OrderTimeElapsed.objects.filter(
            increment_id=self.order.increment_id).last()

        if status in actions_map:
            if status in ['pending', 'scheduled_order']:
                actions_map[status]()
            else:
                actions_map[status](elapsed_obj)
