"""Test cases for order data controller."""

import time

import pytest

from app.core.models import SalesFlatOrder, SalesFlatOrderItem
from app.sale_order.lib import OrderDataController


@pytest.mark.django_db
class TestOrderDataController:
    """Test cases"""

    def test_order_data(self, mock_user, generate_mock_order):
        """To get the required order details

        Asserts:

            Check whether the order details are fetched or not.

        """
        order_controller = OrderDataController(
            generate_mock_order.increment_id)
        order_data = order_controller.order_details()

        assert generate_mock_order.increment_id == order_data[
            0]['increment_id']

    def test_item_weight_update(self, mock_user, generate_mock_order):
        """Test item weight update.

        Asserts:
            Checks whether grams for a product has been converted into kgm's


        """
        # fetch mock order item object
        item_obj = SalesFlatOrderItem.objects.filter(
            order=generate_mock_order)[0]

        order_controller = OrderDataController(
            generate_mock_order.increment_id)

        # update item weight
        order_data = order_controller.item_weight_update(
            [{'item_id': item_obj.item_id, 'weight': 250}])

        # fetch item object
        item_obj = SalesFlatOrderItem.objects.filter(
            order=generate_mock_order)[0]

        assert item_obj.weight == float(0.25)
