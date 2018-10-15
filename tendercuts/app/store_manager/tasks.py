"""Sending order's status sms to the customer related celery tasks."""

import logging

from config.celery import app

from app.core.lib.celery import TenderCutsTask
from app.inventory.lib import InventoryRequestController
from app.store_manager.lib import InventoryFlockAppController

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def mark_out_of_stock():
    """auto approve"""

    requests = InventoryRequestController.auto_approve_expired_request()
    InventoryFlockAppController(requests).publish_request(
        template=InventoryFlockAppController.CRON_AUTO_TEMPLATE)
