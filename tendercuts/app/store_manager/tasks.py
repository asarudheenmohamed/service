"""Sending order's status sms to the customer related celery tasks."""

import logging
import datetime

from config.celery import app

from app.core.lib.celery import TenderCutsTask
from app.inventory.models import InventoryRequest

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def mark_out_of_stock():
    """auto approve"""
    start = datetime.date.today()
    end = datetime.datetime.now() - datetime.timedelta(minutes=15)

    requests = InventoryRequest.objects.filter(
        created_time__gt=start, created_time__lte=end)

    requests.update(status=InventoryRequest.Status.APPROVED.value)
