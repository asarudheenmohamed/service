from .lib.controller import PaymentAutomationController
from .lib.gateway import Payu
from config.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def cancel_payu_orders():

    gw = Payu(log=logger)
    controller = PaymentAutomationController(gw, log=logger)
    controller.cancel_pending_orders(dry_run=False)
