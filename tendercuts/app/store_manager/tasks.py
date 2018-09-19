"""Sending order's status sms to the customer related celery tasks."""

import logging
import datetime

from config.celery import app

from app.core.lib.celery import TenderCutsTask
from app.inventory.models import InventoryRequest
from app.core.models import Graminventory
from app.inventory.lib import InventoryRequestController
from app.store_manager.lib import InventoryFlockAppController

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def mark_out_of_stock():
    """auto approve"""

    start = datetime.date.today()
    end = datetime.datetime.now() - datetime.timedelta(minutes=15)

    requests = InventoryRequest.objects.filter(
        created_time__gt=start,
        created_time__lte=end,
        status__in=InventoryRequest.Status.CREATED.value
    )


    for request in requests:  # type: InventoryRequest

        message = "Marked done automatically for request raised by {}".format(
            request.triggered_by.email
        )
        req_controller = InventoryRequestController(request)
        req_controller.approve(message)

        flock_msg_controller = InventoryFlockAppController(request)
        flock_msg_controller.publish_response('AUTO')

