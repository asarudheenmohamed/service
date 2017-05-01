from .lib.controller import PaymentAutomationController
from .lib.gateway import Payu
from config.celery import app
from celery.utils.log import get_task_logger
from app.core.lib.communication import Flock

logger = get_task_logger(__name__)

@app.task
def cancel_payu_orders():

    gw = Payu(log=logger)
    controller = PaymentAutomationController(gw, log=logger)
    controller.cancel_pending_orders(dry_run=False)


@app.task
def print_refundable_payu_orders():

    gw = Payu(log=logger)
    controller = PaymentAutomationController(gw, log=logger)
    controller.refund_payu_cancelled_orders()


@app.task
def print_failed_to_capture_payments():

    gw = Payu(log=logger)
    controller = PaymentAutomationController(gw, log=logger)
    order_ids = controller.detect_failed_to_capture_payments()

    if len(order_ids) > 0:
        message = ("CRITICAL: We have not received the payment for the following " .
                "orders but have started processing them. @callcenter please follow up. " .
                "Orders: {}").format(", ".join(order_ids))

    return order_ids
