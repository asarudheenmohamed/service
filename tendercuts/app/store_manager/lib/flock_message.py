"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging

from django.conf import settings

from app.core.lib.communication import Flock
from app.inventory.models import InventoryRequest

logger = logging.getLogger(__name__)


class InventoryFlockAppController(object):
    """
    Update order status
    """
    PUBLISH_TEMPLATE = """<flockml>has requested the product: <b>{product}</b> to be marked as out of stock at store: <b>{store}</b>.
Note: This will be auto approved, in the next 15 mins
<b><action id="{id}-1" type="sendEvent">Approve</action></b>
<b><action id="{id}-2" type="sendEvent">Reject</action></b></flockml>"""

    TEMPLATES = {
        'APPROVED': """<flockml><b>SUCCESS:</b> The product: <b>{product}</b> has been marked as out of stock at store <b>{store}</b></flockml>""",
        'REJECTED': """<flockml><b>REJECTED:</b> The product: <b>{product}</b> request has been rejected at <b>{store}</b></flockml>""",
        'FAILED': """<flockml><b>FAILED:</b> The product: <b>{product}</b> has not been marked as out of stock at store  <b>{store}</b></flockml>""",
        'AUTO': """<flockml><b>AUTO:</b> The product: <b>{product}</b> has been marked as out of stock at store <b>{store}</b> automatically</flockml>"""
    }

    def __init__(self, request):
        self.request = request

    @property
    def flock(self):
        return Flock("INV")

    def publish_request(self):
        """Publish the inventory change request in the flock group

        :type request: InventoryRequest
        """
        template = self.PUBLISH_TEMPLATE.format(
            product=self.request.product_name,
            store=self.request.store_name,
            id=self.request.id,
            url=settings.FLOCK_ENDPOINTS['APPROVE_INV_REQ']
        )

        self.flock.send_flockml('SCRUM', template, 'OoS Request', '',
                                send_as=self.request.triggered_by.username)

    def publish_response(self, template):
        """Publish the inventory request's response to the flock group

        :type request: InventoryRequest
        """
        template = self.TEMPLATES[template]
        self.flock.send_flockml(
            'SCRUM',
            template.format(
                product=self.request.product_name,
                store=self.request.store_name),
            'OoS Request',
            '')
