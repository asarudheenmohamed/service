"""
Responsible for controlling order statuses, acts as a bridge between the
magento and python layer
"""

import logging

from django.conf import settings
import collections


from app.core.lib.communication import Flock
from app.inventory.models import InventoryRequest

logger = logging.getLogger(__name__)


class InventoryFlockAppController(object):
    """
    Update order status
    """
    PUBLISH_TEMPLATE = """<flockml>has requested the following inventory to updated at store: <b>{store}</b> for <b>{type}</b>.<br/>{products}Note: This will be auto approved, in the next 15 mins</flockml>"""
    AUTO_TEMPLATE = """<flockml>has updated the following inventory at store: <b>{store}</b> for <b>{type}</b>.<br/>{products}</flockml>"""

    TEMPLATES = {
        'APPROVED': """<flockml><b>SUCCESS:</b> The product: <b>{product}</b> has been marked as out of stock at store <b>{store}</b></flockml>""",
        'REJECTED': """<flockml><b>REJECTED:</b> The product: <b>{product}</b> request has been rejected at <b>{store}</b></flockml>""",
        'FAILED': """<flockml><b>FAILED:</b> The product: <b>{product}</b> has not been marked as out of stock at store  <b>{store}</b></flockml>""",
        'AUTO': """<flockml><b>AUTO:</b> The product: <b>{product}</b> has been updated to {packs} packs at store <b>{store}</b> for {inv_type} inventory automatically</flockml>""",
        'FINISHED': """<flockml><b>ALREADY COMPLETE:</b> The product: <b>{product}</b> request at store <b>{store}</b> has already been completed.</flockml>"""
    }

    def send_approval_messages(cls, requests):
        for request in requests:
            flock_msg_controller = cls(request)
            flock_msg_controller.publish_response('AUTO')
    #
    def __init__(self, request):
        if not isinstance(request, collections.Iterable):
            self.request = [request]
        else:
            self.request = list(request)

    @property
    def flock(self):
        return Flock("INV")

    def _construct_message(self):
        message = ""
        template = "<b>{product}</b> - <b>{qty} Packs</b><br/>"
        for request in self.request: # type: InventoryRequest
            message += template.format(
                product=request.product_name,
                qty=request.qty)

        return message

    def publish_request(self, template=None):
        """Publish the inventory change request in the flock group

        :type request: InventoryRequest
        """
        if not getattr(settings, 'FLOCK_ENDPOINTS', None):
            return

        template = self.PUBLISH_TEMPLATE if not template else template

        sample = self.request[0] #  type: InventoryRequest
        inventory_type = "Today" if sample.type == InventoryRequest.INV_TYPE.TODAY.value \
            else "Tomorrow"
        template = template.format(
            products=self._construct_message(),
            type=inventory_type,
            store=sample.store_name,
            url=settings.FLOCK_ENDPOINTS['APPROVE_INV_REQ']
        )

        self.flock.send_flockml('INVENTORY', template, 'OoS Request', '',
                                send_as=sample.triggered_by.username)

    def publish_response(self, template):
        """Publish the inventory request's response to the flock group

        :type request: InventoryRequest
        """
        template = self.TEMPLATES[template]
        self.flock.send_flockml(
            'INVENTORY',
            template.format(
                product=self.request.product_name,
                store=self.request.store_name),
            'OoS Request',
            '')

