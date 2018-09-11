"""
ALl payment related celery tasks.
"""

import datetime

from celery.utils.log import get_task_logger

from app.core import models as core_models
from app.core.lib import order_controller as controller
from app.core.lib import magento
from app.core.lib.celery import TenderCutsTask
from config.celery import app

logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask)
def cancel_payment_pending_orders():
    """Celery Task to set payment received flag.

    We look for orders in the last 30 mins
    """
    return
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
        try:
            controller.OrderController(conn, order).cancel()
            logger.info("cancelled the order {}".format(inc_id))

            result.append(inc_id)

        except Exception as e:
            # err why ?
            pass

    return result


@app.task(base=TenderCutsTask)
def order_success(order_id):
    """Trigger juspayorder success processor.
    Params:
     order_id(str):order increment_id
    """
    from .lib.gateway.juspay import JuspayOrderSuccessProcessor
    JuspayOrderSuccessProcessor.from_payload(order_id).execute()
