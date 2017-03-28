from .lib.controller import PaymentAutomationController
from .lib.gateway import Payu
from config.celery import app

@app.task
def cancel_payu_orders():
    gw = Payu()
    controller = PaymentAutomationController(gw)
    controller.cancel_pending_orders(dry_run=False)
