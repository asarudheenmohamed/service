"""Consumer for order state changes."""

from celery.utils.log import get_task_logger

from app.core.lib.celery import TenderCutsTask
from app.core.models import SalesFlatOrder
from config.celery import app
from app.core.lib import cache

from .lib import OrderTimeElapsedController

logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def log_message(*args, **kwargs):
    """Celery Task to log messages."""
    print(kwargs)


@app.task(base=TenderCutsTask)
def update_order_elapsed_time(order_id, status):
    """Update order time lapse.

    Params:
     order_id(str):order increment_id
     status(str):order status

    """
    order_obj = SalesFlatOrder.objects.filter(
        increment_id=str(order_id)).last()

    controller = OrderTimeElapsedController(order_obj)
    controller.compute_order_status_elapsed_time(status)
