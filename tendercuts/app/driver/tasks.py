"""Sending order's status sms to the customer related celry tasks."""

from datetime import datetime, timedelta
import logging

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import SMS
from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.driver.models import DriverLoginLogout
from config.celery import app
from django.conf import settings


logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def driver_stat(order_id):
    """Celery task to add the driver completed order."""
    from app.driver.lib.driver_stat_controller import DriverStatController

    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id).last()
    if not order_obj:
        raise ValueError('Order object Does not exist')

    stat_controller = DriverStatController(order_id)
    orders = stat_controller.generate_stat(
        order_obj.increment_id, order_obj.status)


@app.task(base=TenderCutsTask, ignore_result=True)
def generate_end_of_day_driver_stat(order_id):
    """Celery task to generate end of day driver status."""
    from app.driver.lib.end_of_day_driver_status import DriverStatusController
    controller = DriverStatusController()
    controller.generate_driver_completed_order_status()


@app.task(base=TenderCutsTask, ignore_result=True)
def customer_current_location(customer_id, lat, lon):
    """Update customer current location.

    Params:
     customer_id(int):user entity_id
     lat(int):custoner location latitude
     lon(int):customer location longitude

    """

    from app.driver.lib.customer_location import CustomerLocationController
    customer_location_controller = CustomerLocationController()
    customer_loc_obj = customer_location_controller.update_customer_location(
        customer_id, lat, lon)


@app.task(base=TenderCutsTask, ignore_result=True)
def send_sms(order_id):
    """Celery task to send the order's status to the customer."""

    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)

    if not order_obj:

        raise ValueError('Order object Does not exist')

    order_obj = order_obj.last()

    customer = CustomerSearchController.load_basic_info(
        order_obj.customer_id)

    logger.info("Send status as {} to the customer : {}".format(
        order_obj.status, customer[0]))

    if order_obj.medium == 4:

        message = settings.RETAIL_ORDER_STATUS_MESSAGE[
            order_obj.status].format(customer[4])

        scheduled_time = datetime.now() + timedelta(hours=4)
        scheduled_time = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")

        sheduled_message = settings.RETAIL_ORDER_STATUS_SHEDULED_MESSAGE[
            'complete']

        # sheduled the order like and dislike message
        SMS().send_scheduled_sms(scheduled_time, customer[2],
                                 sheduled_message)

        logger.info(
            "Sheduled the product like and dislike message for this customer:{}".format(
                customer[4]))

    else:
        message = settings.ONLINE_ORDER_STATUS_MESSAGE[
            'processing'].format(
            order_obj.increment_id)

    SMS().send_sms(customer[2], message)


@app.task(base=TenderCutsTask, ignore_result=True)
def set_checkout():
    """Celery task to set Check Out time for the driver."""
    objs = DriverLoginLogout.objects.filter(
        date=datetime.date.today(), check_out__isnull=True)

    logger.info(
        "To Update the check_out time for the drivers who forgot to check_out")

    if objs:
        objs.select_related('driver').update(
            check_out=datetime.now().time().replace(
                hour=23, minute=59, second=0, microsecond=0))
