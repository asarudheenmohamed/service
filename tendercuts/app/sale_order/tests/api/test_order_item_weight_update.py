"""Test order item weight update."""

import pytest
from app.core.models.sales_order import SalesFlatOrderItem
from app.driver.models import DriverOrder


@pytest.mark.django_db
class TestUpdateWeight:

    def test_product_weight_update(
            self,
            auth_rest,
            generate_mock_order):
        """Test order item weight update.

        Params:
            auth_rest(pytest fixture):user requests

        Asserts:
            Check response not equal to None
            Check response status and message

        """
        # fetch the sale order item object
        sales_flat_order_item = SalesFlatOrderItem.objects.filter(
            order=generate_mock_order)
        data = {
            'increment_id': sales_flat_order_item[0].order.increment_id,
            'items': [{'item_id': sales_flat_order_item[0].item_id,
                       'weight':7}]}

        response = auth_rest.post(
            "/sale_order/item_weight/", data,
            format='json')
        assert (response) is not None
        assert response.status_code == 200
        assert response.data['status'] == True
        assert response.data['message'] == "successfully weight update"
