"""
ALl payment related celery tasks.
"""

import datetime
from config.celery import app
from celery.utils.log import get_task_logger

from app.core.lib import order_controller as controller
from app.core.lib import magento
from app.core.lib.celery import TenderCutsTask
from app.core import models as core_models

logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask)
def cancel_payment_pending_orders():
    """Celery Task to set payment received flag.

    We look for orders in the last 30 mins
    """
    THRESHOLD = 30 * 60   # 30 mins
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=THRESHOLD)
    conn = magento.Connector()

    payment_pending_orders = core_models.SalesFlatOrder.objects   \
        .filter(status='pending_payment', created_at__lt=start) \
        .prefetch_related('payment')

    result = []
    for order in payment_pending_orders:
        inc_id = order.increment_id
        logger.info("cancelling the order {}".format(inc_id))
        try:
            controller.OrderController(conn, order).cancel()
            result.append(inc_id)
        except Exception as e:
            # err why ?
            pass

    return result

