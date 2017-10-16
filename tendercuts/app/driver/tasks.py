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

    SMS().send(customer[2], order_obj[0].status)
