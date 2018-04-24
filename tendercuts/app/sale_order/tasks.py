"""Consumer for order state changes."""

from celery.utils.log import get_task_logger

from app.core.lib.celery import TenderCutsTask
from app.core.models import SalesFlatOrder
from config.celery import app

from .lib.order_time_elapse_controller import OrderTimelapseController

logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def log_message(*args, **kwargs):
    """Celery Task to log messages."""
    print(kwargs)


@app.task(base=TenderCutsTask, ignore_result=True)
def update_order_lapse(order_id):
    """Update order time lapse.

    Params:
     order_id(str):order increment_id

    """
    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id).last()
    controller = OrderTimelapseController(order_obj)

    methods = {'processing': controller.compute_order_pending_time_elapse,
               'out_delivery': controller.compute_order_out_delivery_time_elapse,
               'complete': controller.compute_order_out_delivery_time_elapse
               }

    methods[order_obj.status]()
