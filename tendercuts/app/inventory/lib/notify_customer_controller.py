"""All notify customer controller related actions."""
import datetime
import logging

import dateutil.parser
import pytz
from django.db.models import Q
from django.utils import timezone

from app.core.models.inventory import GraminventoryLatest
from app.inventory.models import NotifyCustomer

logger = logging.getLogger(__name__)


class NotifyCustomerController(object):
    """Notify Customer Controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_customer_notify_obj(self):
        """To get the NotifyCustomer objects.

        Returns:
            notify_obj

        """
        yesterday = timezone.now().replace(
            hour=20,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=pytz.utc)-datetime.timedelta(days=1)

        logger.debug(
            "To fetch the unnotified NotifyCustomer objects from {} to {}".format(
                yesterday, timezone.now()))

        notify_obj = NotifyCustomer.objects.select_related('customer').filter(
            created_at__range=(yesterday, timezone.now()),
            isnotified=False)

        return notify_obj

    def get_avalible_notifies(self, notify_objs):
        """To get the available products of customer notifies.

        Params:
            notify_objs: notify_obj

        Returns:
            customers_notify

        """
        inventory_dict = {}
        customers_order = {}
        customers_notify = {}
        available_product = {}

        for notify_obj in notify_objs:
            customers_order.setdefault((
                notify_obj.store_id, notify_obj.product_id), []).append(notify_obj.customer.username)

        inventory_objs = GraminventoryLatest.objects.select_related('product').filter(qty__gt=0)

        for inventory_obj in inventory_objs:
            inventory_dict[(inventory_obj.store_id, inventory_obj.product_id)] = inventory_obj.qty

        logger.debug(
            "To check NotifyCustomer products{} are available in GraminventoryLatest{}".format(
                customers_order, inventory_dict))

        for inventory in inventory_dict:
            if inventory in customers_order.keys():
                available_product[inventory] = list(set(customers_order[inventory]))

        if not available_product:
                raise ValueError('Notify customer orders are not available')

        for product in available_product:
            for customer in available_product[product]:
                customers_notify.setdefault(customer, []).append(product)

        logger.info("consoldated the available products to each customers: {}".format(
            customers_notify))

        return customers_notify

    def update_isnotified(self, notify_obj, notify_customer):
        """To set NotifyCustomer object as notified.

        Params:
            notify_obj: notify_obj
            notify_customer: (dict)notify_customers

        Returns:
            customers_notify

        """
        products_list = []

        for products in notify_customer:
            products_list.extend(notify_customer[products])

        logger.debug("To make single query to filter all products{} in singleshot".format(
            products_list))

        queries = [Q(store_id=value[0], product_id=value[1]) for value in list(set(products_list))]
        query = queries.pop()

        for item in queries:
            query |= item

        logger.info("To set the field isnotified as True for Notified customers")

        notify_obj.select_related('customer').filter(query).update(isnotified=True)

