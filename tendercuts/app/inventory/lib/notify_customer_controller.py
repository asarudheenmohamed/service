"""All notify customer controller related actions."""
import datetime
import logging

import dateutil.parser
import pandas as pd
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
            "Get the unnotified NotifyCustomer objects from {} to {}".format(
                yesterday, timezone.now()))

        notify_obj = NotifyCustomer.objects.select_related('customer').filter(
            created_at__range=(yesterday, timezone.now()),
            is_notified=False)

        return notify_obj

    def get_avalible_notifies(self, notify_objs):
        """To get the available products of customer notifies.

        Params:
            notify_objs: notify_obj

        Returns:
            customers_notify

        """
        # Create the DataFrame for notify_objs
        columns = ['id', 'product_id', 'store_id', 'customer']
        notify_df = notify_objs.values_list(*columns)
        notify_df = pd.DataFrame(list(notify_df), columns=columns)

        # Create the DataFrame for inventory_objs
        columns = ['product_id', 'store_id', 'qty']
        inventory_objs = GraminventoryLatest.objects.select_related(
            'product').filter(qty__gt=0).values_list(*columns)
        inventory_df = pd.DataFrame(list(inventory_objs), columns=columns)

        # Merge the dataframe: Prepare the indexes for joining
        notify_df = notify_df.set_index(['product_id', 'store_id'])
        inventory_df = inventory_df.set_index(['product_id', 'store_id'])

        logger.debug(
            "To join the notify:{} and inventory:{} DataFrames".format(
                notify_df, inventory_df))
        # Use inner join to get only the matched Rows
        notify_df = notify_df.join(inventory_df, how='inner')

        logger.debug("To groupby the joined DataFrame with customer")

        customers_order = {}

        def format_df(group):
            customer_id = group.customer.tolist()[0]
            customers_order[customer_id] = group[['product_id', 'store_id', 'id']].to_dict('records')

        notify_df.reset_index().groupby('customer').apply(format_df)

        logger.debug("Fetched the customers list of notifies: {}".format(
            customers_order))

        customers_notify = {}
        id_list = []
        for customer_id, products in customers_order.items():
            product_list = []
            for product in products:
                # list the notified products id
                id_list.append(product['id'])
                product_list.append(
                    (product['product_id'], product['store_id']))
            # remove the duplicate notify products for each customers
            customers_notify[customer_id] = list(set(product_list))

        logger.debug(
            "Change is_notified as True for the notification ids:{}".format(
                id_list))

        notify_objs.select_related(
            'customer').filter(id__in=id_list).update(is_notified=True)

        return customers_notify
