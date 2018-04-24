"""Order time lapse controller."""
import datetime
import logging

import dateutil.parser
import pytz
from django.contrib.auth.models import User
from django.utils import timezone

from app.core.lib.exceptions import CustomerNotFound
from app.core.models import SalesFlatOrder, SalesFlatOrderItem
from app.core.models.customer import CustomerEntityVarchar
from app.sale_order.models import OrderTimelapse

# Get an instance of a logger
logger = logging.getLogger(__name__)


class OrderTimelapseController(object):
    """Order time lapse controller."""

    def __init__(self, order):
        """Constructor."""
        self.order = order

    def schedule_order_start_time(self):
        """Returns the Scheduled order Starting Time.
        """
        SLOTS = {52: "7:00 - 9:00",
                 53: "9:00 - 11:00",
                 54: "11:00 - 13:00",
                 55: "17:00 - 19:00",
                 56: "19:00 - 21:00"}

        promised_time = None
        tz = pytz.timezone('Asia/Kolkata')

        date_obj = self.order.scheduled_date

        timetext = self.order.scheduled_slot
        timetext = SLOTS[timetext].split("-")
        timetext = timetext[0]

        logger.debug(
            "Formatting {}: {} to text".format(
                date_obj, timetext))

        promised_time = dateutil.parser.parse(
            "{} {}".format(date_obj, timetext))

        return promised_time

    def spending_time(self, status_start_time=None):
        """Calculate order status spending time.

        Params:
         status_start_time(datetime): status starting time

        """
        if self.order.deliverytype == 2:

            start_time = self.schedule_order_start_time()
        else:
            start_time = self.order.created_at

        if start_time > self.order.updated_at:

            spending_time = (self.order.updated_at.hour - start_time.hour) * \
                60 + self.order.updated_at.minute - start_time.minute
        else:
            status_start_time = status_start_time if status_start_time is not None else start_time

            spending_time = self.order.updated_at - status_start_time
            spending_time = spending_time.seconds / 60

        return spending_time

    def fetch_driver_basic_info(self):
        """Returns to the driver entity object."""
        query_set = CustomerEntityVarchar.objects.filter(
            attribute_id=149, value=self.order.driver_number)

        if len(query_set) == 0:

            raise CustomerNotFound()

        driver = query_set[0]

        return driver

    def compute_order_pending_time_lapse(self):
        """Compute order pending state time lapse."""
        time_spend = self.spending_time()

        # driver object
        driver = self.fetch_driver_basic_info()

        OrderTimelapse.objects.create(
            driver_user=User.objects.get(
                username='u:{}'.format(
                    driver.entity_id)),
            increment_id=self.order.increment_id,
            deliverytype=self.order.deliverytype,
            processing_time=self.order.updated_at,
            pending_lapse=time_spend)

        logger.debug(
            "The order:{} pending state time lapse updated".format(
                self.order.increment_id, self.order.status))

    def compute_order_processing_time_lapse(self):
        """Compute order processing state time lapse."""
        order_lapse_obj = OrderTimelapse.objects.get(
            increment_id=self.order.increment_id)

        processing_lapse = self.spending_time(
            status_start_time=order_lapse_obj.processing_time)

        order_lapse_obj.processing_lapse = processing_lapse
        order_lapse_obj.out_delivery_time = self.order.updated_at

        order_lapse_obj.save()

        logger.debug(
            "The order:{} processing state time lapse updated".format(
                self.order.increment_id, self.order.status))

    def compute_order_out_delivery_time_lapse(self):
        """Compute order out delivery state time lapse."""
        order_lapse_obj = OrderTimelapse.objects.get(
            increment_id=self.order.increment_id)
        out_delivery_lapse = self.spending_time(
            status_start_time=order_lapse_obj.out_delivery_time)
        order_lapse_obj.out_delivery_lapse = out_delivery_lapse

        order_lapse_obj.completed_time = self.order.updated_at

        order_lapse_obj.save()

        logger.debug(
            "The order:{} out delivery state time lapse updated".format(
                self.order.increment_id, self.order.status))
