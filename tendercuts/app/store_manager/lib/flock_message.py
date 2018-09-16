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
        has request the product: {product} to be marked as out of stock at {store}<br/>
        Note: This will be auto approved, in the next 15 mins<br/>
        <b><action id="{id}-1" type="sendEvent">Approve</action></b><br/>
        <b><action id="{id}-2" type="sendEvent">Reject</action></b><br/>
        </flockml>"""

    SUCCESS_TEMPLATE = """<flockml>
        The product: {product} has been marked as out of stock <br/>
        </flockml>"""

    FAILED_TEMPLATE = """<flockml>
        FAILED: The product: {product} has not been marked as out of stock <br/>
        </flockml>"""

    def __init__(self):
        pass

    @property
    def flock(self):
        return Flock("INV")

    def publish_request(self, request):
        """Publish the inventory change request in the flock group

        :type request: InventoryRequest
        """
        template = self.PUBLISH_TEMPLATE.format(
            product=request.product_name,
            store=request.store_name,
            id=request.id,
            url=settings.FLOCK_ENDPOINTS['APPROVE_INV_REQ']
        )

        self.flock.send_flockml('SCRUM', template, 'OoS Request', '',
            send_as=request.triggered_by.username)

    def publish_respone(self, request, success=True):
        """Publish the inventory change request in the flock group

        :type request: InventoryRequest
        """
        template = self.SUCCESS_TEMPLATE if success else self.FAILED_TEMPLATE
        self.flock.send_flockml(
            'SCRUM',
            template.format(product=request.product_name),
            'OoS Request', '')

    def process_action(self, action_data):
        """Process the response from flock user interaction
        https://docs.flock.com/display/flockos/client.flockmlAction

        :type request: InventoryRequest
        :param requst:
        :return:
        """

        # 0 -? approved, 1- rejected
        inv_request_id, action = action_data['actionId'].split("-")
        request = InventoryRequest.objects.get(pk=inv_request_id)
        request.status = action
        request.save()
        # Inventory Processing code here

        self.publish_respone(request, success=True)
