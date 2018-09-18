"""Sending order's status sms to the customer related celery tasks."""

import logging
import datetime

from config.celery import app

from app.core.lib.celery import TenderCutsTask
from app.inventory.models import InventoryRequest
from app.core.models import Graminventory

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def mark_out_of_stock():
    """auto approve"""
    start = datetime.date.today()
    end = datetime.datetime.now() - datetime.timedelta(minutes=15)

    requests = InventoryRequest.objects.filter(
        created_time__gt=start, created_time__lte=end)

    for request in requests:
        inv = Graminventory.objects.filter(
            product_id=request.product_id,
            store_id=request.store_id
        )

        if not inv:
            continue

        inv = inv.first()
        inv.qty = request.qty
        inv.save()

    requests.update(status=InventoryRequest.Status.APPROVED.value)
