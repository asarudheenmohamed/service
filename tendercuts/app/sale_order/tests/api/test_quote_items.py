"""Test customer last created quote."""

import pytest
from app.core.models.sales_order import SalesFlatOrderItem
from app.driver.models import DriverOrder


@pytest.mark.django_db
class TestQuoteItem:

    def test_quote_item_viewset(
            self,
            auth_rest,
            generate_new_order):
        """Test customer last quote item.

        Params:
            auth_rest(pytest fixture):user requests
            generate_new_order(obj): sale order object

        Asserts:
            Check response not equal to None
            Check response customer id is equal to the mock customer id

        """
        response = auth_rest.get(
            "/sale_order/quote_items/", {
                "store_id": generate_new_order.store.store_id, "customer_id": generate_new_order.customer_id},
            format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert response.json()['results'][0][
            'customer_id'] == generate_new_order.customer_id
