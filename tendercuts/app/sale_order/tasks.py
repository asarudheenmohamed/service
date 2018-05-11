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
    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id).last()

    order_status_list = cache.get_key(order_obj.increment_id)

    if order_status_list is None:
        order_status_list = [order_obj.status]
    elif status not in order_status_list:
        order_status_list.append(order_obj.status)
    else:
        return None

    logger.info("Set order:{} status: {} in redis db".format(
        order_id, order_status_list))

    controller = OrderTimeElapsedController(order_obj)
    controller.compute_order_status_elapsed_time(status)

    # set order status list in redis db like
    # ['pending','processing','out_delivery','complete'] it's expire to 24 hours
    cache.set_key(order_obj.increment_id, order_status_list, 60 * 60 * 24)
