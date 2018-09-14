"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging

from app.inventory.models import InventoryRequest
from app.core.lib.communication import Flock
from django.conf import settings

logger = logging.getLogger(__name__)


class InventoryFlockMessageController(object):
    """
    Update order status
    """
    PUBLISH_TEMPLATE = """<flockml>
        has request the product: {product} to be marked as out of stock <br/>
        Note: This will be auto approved, in the next 15 mins<br/>
        <b><action id="{id}-0" type="sendEvent" url="{url}">Approve</action></b>
        <b><action id="{id}-1" type="sendEvent" url="{url}">Reject</action></b>
        </flockml>"""

    def __init__(self):
        pass

    def publish_request(self, request):
        """

        :type request: InventoryRequest
        """
        template = self.PUBLISH_TEMPLATE.format(
            product=request.product_name,
            id=request.id,
            url=settings.FLOCK_ENDPOINTS['APPROVE_INV_REQ']
        )

        Flock().send_flockml('SCRUM', template, 'OoS Request', '',
            send_as=request.triggered_by.first_name)




