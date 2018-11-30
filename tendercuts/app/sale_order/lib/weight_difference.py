"""End point order item weight diff computation."""
import logging
from datetime import datetime
from app.core.models import SalesFlatOrder, SalesFlatOrderItem
from app.core.models.product import CatalogProductFlat1
import pandas as pd
from app.core.models.category import CatalogCategoryEntity
from app.core.models.customer.entity import MCreditBalance, MCreditTransaction
from app.core.models.customer.entity import CustomerEntity

logger = logging.getLogger(__name__)


class OrderWeightDiffController(object):
    """Order Weight diff controller."""

    def __init__(self, order):
        """Constructor."""
        self.order = order

    def add_credit_balance(self, customer_id, amount):
        """update credit balance for the customer.

        Params:
          customer_id(int): customer entity_id
          amount(float): credit balance amount

        """
        balance_obj, status = MCreditBalance.objects.get_or_create(
            customer=CustomerEntity.objects.get(entity_id=customer_id), is_subscribed=1)

        try:
            balance_obj.amount += amount
        except TypeError:
            balance_obj.amount = amount

        balance_obj.save()
        MCreditTransaction.objects.create(
            balance=balance_obj,
            balance_amount=balance_obj.amount,
            balance_delta=amount,
            action='manual',
            message='shell via',
            is_notified=1,
            created_at=datetime.now(),
            updated_at=datetime.now())

        logger.info(
            "updated store credit amount:{} for the customer:{}".format(
                amount, customer_id))

    def compute_order_weight_diff_amount_calc(self):
        """Compute order item weight difference amount.

        Returns:
            Returns the order sea food item dataframe object

        """
        order_object = self.order
        items_sku_and_weight = order_object.items.values(
            'sku', 'qty_ordered', 'weight', 'price', 'row_total')

        logger.debug("Fetched order item details for given order:{}".format(
            self.order.increment_id))
        order_items_df = pd.DataFrame(list(items_sku_and_weight))

        sf_category_item = CatalogCategoryEntity.objects.filter(
            products__sku__in=list(order_items_df['sku']),
            entity_id=14).values(
            'entity_id',
            'products__sku')

        logger.debug("To find sea food SKU objects for the order:{} item".format(
            self.order.increment_id))

        sf_items_df = pd.DataFrame(list(sf_category_item))

        product_objects = CatalogProductFlat1.objects.filter(
            sku__in=list(sf_items_df['products__sku'])).values(
            'weight_from', 'weight_to', 'sku')

        logger.debug("Fetched product objects for the order:{} sea food SKU's:{}".format(
            self.order.increment_id, list(sf_items_df['products__sku'])))

        product_objects_df = pd.DataFrame(list(product_objects))

        items_df = pd.merge(order_items_df, product_objects_df, on='sku')

        items_df = items_df.convert_objects(convert_numeric=True)

        items_df = items_df.drop(
            items_df[
                ((items_df['qty_ordered'] * items_df['weight_to'] / 1000) > items_df.weight) | (((((items_df['weight_to'] - items_df['weight_from']) / 10) + items_df['weight_from']) * items_df['qty_ordered']) / 1000 >= items_df['weight'])].index)

        if items_df.empty:
            return items_df

        logger.debug("To compute the weight diff amount evaluation for the order:{}".format(
            self.order.increment_id))

        items_df['mid_weight'] = (
            ((items_df['weight_to'] -
              items_df['weight_from']) /
             10) +
            items_df['weight_from'])
        items_df['refund_amount'] = (items_df['price'] /
                                     items_df['weight_to'] *
                                     (((items_df['qty_ordered'] *
                                        items_df['mid_weight'] /
                                        1000) -
                                       items_df['weight']) *
                                      1000))

        logger.info("computed weight diff amount evaluation for the order:{} from sea food SKU's:{} computed amount for the weight differs in SKU's:{}".format(
            self.order.increment_id, list(items_df['sku']), list(items_df['refund_amount'])))

        # add credit balance
        self.add_credit_balance(
            order_object.customer_id,
            items_df['refund_amount'].sum().round())

        return items_df
