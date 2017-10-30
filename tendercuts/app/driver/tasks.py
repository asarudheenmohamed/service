"""Sending order's status sms to the customer related celry tasks."""

from config.celery import app
from celery.utils.log import get_task_logger
from app.core.lib.celery import TenderCutsTask
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.communication import SMS
from app.core.models import SalesFlatOrder


logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def driver_stat(order_id):
    """Celery task to add the driver completed order"""
    try:
	    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)
	    stat_controller = DriverStatController(order_id)
	except ValueError:
        print "This order id is invalid"

    orders = stat_controller.generate_stat(
        order_obj.increment_id, order_obj.status)

    logger.info("No of order is added to driver : {}".format(
        order_obj[0].driver_id))
