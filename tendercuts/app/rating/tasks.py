"""Rating module celery tasks."""

import logging

from app.core.lib.celery import TenderCutsTask
from app.rating.lib.rating_controller import RatingController
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def create_fresh_desk_ticket(order_id):
    """Celery task to create fresh desk ticket."""

    controller = RatingController(order_id)

    controller.create_fresh_desk_ticket()
