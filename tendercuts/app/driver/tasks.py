from .lib import ShadowFaxDriverController
from config.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def push_orders_to_shawdowfax():
	controller = ShadowFaxDriverController(log=logger)
        responses = controller.push_orders()
        return responses
