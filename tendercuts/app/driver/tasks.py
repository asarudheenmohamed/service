"""Sending order's status sms to the customer related celry tasks."""

from config.celery import app
from celery.utils.log import get_task_logger
from app.core.lib.celery import TenderCutsTask
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.communication import SMS
from app.core.models import SalesFlatOrder


logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def send_sms(order_id):
    """Celery task to send the order's status to the customer."""
    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)
    customer = CustomerSearchController.load_basic_info(
        order_obj[0].customer_id)

    logger.info("Send status as {} to the customer : {}".format(
        order_obj[0].status, customer[0]))

    SMS().send(9952267549, order_obj[0].status)


@app.task(base=TenderCutsTask, ignore_result=True)
def driver_stat(order_id):
    """Celery task to add the driver completed order"""
    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)
    stat_controller = DriverStatController()
    orders = stat_controller.generate_stat(
        order_obj.increment_id, order_obj.status)

    logger.info("No of order is added to driver : {}".format(
        order_obj[0].driver_id))
