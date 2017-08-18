"""Consumer for order state changes."""

from config.celery import app
from celery.utils.log import get_task_logger

from app.core.lib.celery import TenderCutsTask

logger = get_task_logger(__name__)


@app.task(base=TenderCutsTask)
def log_message(*args, **kwargs):
    """Celery Task to log messages."""
    print (kwargs)


