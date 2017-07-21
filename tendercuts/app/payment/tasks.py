"""
ALl payment related celery tasks.
"""

import datetime
from config.celery import app
from celery.utils.log import get_task_logger

from app.core.lib import order_controller as controller
from app.core.lib.celery import TenderCutsTask
from app.core import models as core_models
from app.payment import lib

logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask)
def check_payment_status():
    """Celery Task to set payment received flag.

    We look for orders in the last 30 mins
    """
    THRESHOLD = 30 * 60   # 30 mins
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=THRESHOLD)

    payment_pending_orders = core_models.SalesFlatOrder.objects           \
        .filter(status='pending', created_at__range=[start, end]) \
        .prefetch_related('payment')

    for order in payment_pending_orders:
        inc_id = order.increment_id
        logger.info("Verifying the status of {}".format(inc_id))
        method = order.payment.first().method

        if not method:
            logger.error(
                "Unable to find the payment method for {}").format(inc_id)
            continue

        if method == "cashondelivery":
             # ignore COD
             continue

        logger.info("querying {} for the payment status of {}".format(
            method, inc_id)) 

        gateway = lib.gateway.get_gateway_by_method(method)
        status = gateway().check_payment_status(inc_id)

        logger.info("Got status as {} from PG: {} for ORD: {}".format(
            status, method, inc_id))

        if status:
            # set the payment received flag to true
            controller.OrderController(None, order).update_payment_status()
