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
from app.driver import tasks

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
        order_controller = controller.OrderController(conn, order)
        # check if the order is payubiz payment method
        if order.is_payu:
            from app.payment.lib.gateway.payu import Payu
            if Payu().check_payment_status(inc_id):
                order_controller.payment_success(
                    is_comment='Payment verified from payubiz')
                logger.info(
                    'Payment verified from payubiz for this order: {}'.format(inc_id))

                tasks.send_sms.delay(inc_id, 'payment_confirmation')

                logger.info(
                    "Sent payment confirmation message to the order:{} ".format(
                        inc_id))
                continue

        try:
            order_controller.cancel()
            logger.info("cancelled the order {}".format(inc_id))

            tasks.send_sms.delay(
                inc_id,
                'payment_pending_to_cancel')
            logger.info(
                "message sent while payment pending to cancel the order:{} ".format(
                    inc_id))

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
