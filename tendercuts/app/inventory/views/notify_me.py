"""Endpoints to provide customer notifications."""
import logging

from rest_framework import mixins, viewsets

from app.inventory.serializers import NotifyCustomerSerializer

logger = logging.getLogger(__name__)


class CustomerNotificationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Endpoint to update the customer's order.

    EndPoint:
        API: inventory/notify_me/

    """

    serializer_class = NotifyCustomerSerializer

    def create(self, request, *args, **kwargs):
        """To create customer order object.

        Input:
            product_id(int) = customer's ordered product id,
            store_id(int) = customer's ordered store id

        returns:
            Created NotifyCustomer object

        """
        request.data.update({'customer': self.request.user.id})
        super(CustomerNotificationViewSet, self).create(
         request, *args, **kwargs)

        logger.info(
            "To create the NotifyCustomer objects for the user: {}".format(
                self.request.user.id))

        return super(CustomerNotificationViewSet, self).create(
            request, *args, **kwargs)
