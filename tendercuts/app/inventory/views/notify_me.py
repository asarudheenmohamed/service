"""Endpoints to provide customer notifications."""

import logging

import pytz
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from app.core.lib.utils import get_user_id
from app.inventory.lib import NotifyCustomerController

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CustomerNotificationViewSet(viewsets.ModelViewSet):
    """Endpoint to update the customer's order.

    EndPoint:
        API: inventory/notify_me/

    """

    def create(self, request, *args, **kwargs):
        """To create customer order object.

        Input:
            product_id(int) = customer's ordered product id,
            store_id(int) = customer's ordered store id

        returns:
            status

        """
        product_id = self.request.data['product_id']
        store_id = self.request.data['store_id']
        user_id = get_user_id(self.request)

        controller = NotifyCustomerController(user_id)
        user = controller.get_user_obj()
        notify_obj = controller.create_notify(user, store_id, product_id)

        logger.info(
            'Notification object was created for the user: {}.'
            .format(user_id))

        return Response({'status': True})
