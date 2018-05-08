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

    def _update_order_elapsed_time(self, ela_obj):
        """Compute order status elapsed time and update.

        Params:
         ela_obj(obj): elapsed object

        """
        time_elapsed = lambda ending_time, starting_time: round(((ending_time -
                                                                  starting_time).total_seconds()) / 60, 0)
        if self.order.deliverytype == 1:
            ela_obj.pending_elapsed = time_elapsed(
                ela_obj.processing_time, ela_obj.pending_time)

            ela_obj.processing_elapsed = time_elapsed(
                ela_obj.out_delivery_time, ela_obj.processing_time)

            ela_obj.out_delivery_elapsed = time_elapsed(
                ela_obj.completed_time, ela_obj.out_delivery_time)

        if self.order.deliverytype == 2:

            promised_time = dateutil.parser.parse(
                "{} {}".format(self.order.scheduled_date, self.slots[self.order.scheduled_slot]))

            if ela_obj.processing_time > promised_time:
                ela_obj.pending_elapsed = time_elapsed(
                    ela_obj.processing_time, promised_time)
            else:
                ela_obj.pending_elapsed = 0

            if ela_obj.out_delivery_time > promised_time:
                processing_elapse = time_elapsed(
                    ela_obj.out_delivery_time, promised_time)

                ela_obj.out_delivery_elapsed = time_elapsed(
                    ela_obj.completed_time, ela_obj.out_delivery_time)

            else:
                ela_obj.processing_elapsed = 0

                ela_obj.out_delivery_elapsed = time_elapsed(
                    ela_obj.completed_time, promised_time)

        ela_obj.save()

        logger.info("order id:{} pending elapsed:{},processing elapsed:{},out_deliver elapsed:{} time computed.".format(
            self.order.increment_id, ela_obj.pending_elapsed, ela_obj.processing_elapsed, ela_obj.out_delivery_elapsed))

    def fetch_driver_basic_info(self):
        """Returns to the driver entity object."""
        query_set = CustomerEntityVarchar.objects.filter(
            attribute_id=149, value=self.order.driver_number)

        if len(query_set) == 0:

            raise CustomerNotFound()

        driver = query_set[0]

        return driver

    def update_order_status_time(self, status):
        """Update order state time and elapsed time."""

        # driver object

        driver = self.fetch_driver_basic_info()
        if status == 'pending':

            OrderTimeElapsed.objects.create(
                increment_id=self.order.increment_id,
                deliverytype=self.order.deliverytype,
                pending_time=timezone.now(),
                created_at=timezone.now())

            logger.info("Creating order elapsed object for order id:{}".format(
                self.order.increment_id))

        elapsed_obj = OrderTimeElapsed.objects.get(
            increment_id=self.order.increment_id)

        if status == 'processing':

            elapsed_obj.driver_user = User.objects.get(
                username='u:{}'.format(driver.entity_id))
            elapsed_obj.processing_time = timezone.now()
            elapsed_obj.save()

            logger.info("Update a processing time:{} for order id:{}".format(
                timezone.now(), self.order.increment_id))

        elif status == 'out_delivery':
            elapsed_obj.out_delivery_time = timezone.now()
            elapsed_obj.save()

            logger.info("Update a out_delivery time:{} for order id:{}".format(
                timezone.now(), self.order.increment_id))

        elif status == 'complete':
            elapsed_obj.completed_time = timezone.now()
            elapsed_obj.save()

            logger.info("Update a completed time:{} for  order id:{}".format(
                timezone.now(), self.order.increment_id))

            self._update_order_elapsed_time(elapsed_obj)
