"""Test driver order fetch."""

import pytest
from app.core.models.sales_order import SalesFlatOrderItem
from app.driver.models import DriverOrder


@pytest.mark.django_db
class TestUpdateWeight:

    def test_product_weight_update(
            self,
            auth_rest,
            generate_mock_order):
        """Test the product weight update.

        Params:
            auth_rest(pytest fixture):user requests

        Asserts:
            Check response not equal to None
            Check response weight is equal to to the custom weight

        """
        # fetch the sale order item object
        sales_flat_order_item = SalesFlatOrderItem.objects.filter(
            order=generate_mock_order)
        data = {
            'item_id': sales_flat_order_item[0].item_id,
            'weight': 7,  # custom weight
            'row_total': sales_flat_order_item[0].row_total}

        # put the values in product update end point
        response = auth_rest.put(
            "/driver/driver/product_weight/update/{}/".format(
                sales_flat_order_item[0].item_id), data,
            format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert float(response.data['weight']) == float(7)
