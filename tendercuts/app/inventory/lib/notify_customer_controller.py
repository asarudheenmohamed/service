"""All Customer notification related actions."""
import logging

from django.contrib.auth.models import User

from app.inventory.models import NotifyCustomer

logger = logging.getLogger(__name__)


class NotifyCustomerController(object):
    """Order Data controller."""

    # prefix used for customer in django tables.
    PREFIX = "u"

    def __init__(self, customer_id):
        """Constructor."""
        self.customer = customer_id

    def get_user_obj(self):
        """Fetch the order details.

        Params:
            order_id(str):Customer placed order_id

        Returns:
            Returns user

        """
        user_name = ("{}:{}".format("u", self.customer))
        user_obj = User.objects.get(username=user_name)

        return user_obj

    def create_notify(self, user, store_id, product_id):
        """Create customer's notify object.

        Params:
            user_name(str) = customer's name
            product_id(int) = customer's ordered product id,
            store_id(int) = customer's ordered store id

        Returns:
            notify_obj

        """
        notify_obj = NotifyCustomer.objects.create(
            customer=user,
            product_id=product_id,
            store_id=store_id)

        logger.info(
            'Notification object was created for the user: {}'
            .format(self.customer))

        return notify_obj
