"""Test Test promised delivery time and order count based on test user."""
import json
from datetime import datetime

import dateutil.parser
import pytest
import pytz

from app.core.lib.test.utils import *


@pytest.mark.django_db
class TestOrder:
    """Test placed order's sku."""

    def test_store_orders(self, auth_rest, mock_user):
        """Test placed order sku and quqntity.

        Params:
        auth_rest(pytest fixture):user requests
        test_user(int):Test user id

        Assers:
         1.Test placed order sku

        """
        order_obj = GenerateOrder()
        order_obj = order_obj.generate_order(
                mock_user.entity_id,
                scheduled_order=True,
                product_id=[(196, 1)])

        orders = auth_rest.get(
            "/sale_order/store_order/?store_id={}&sku={}&deliverydate={}"
            .format(7, 'CHK_LEG_SKIN_OFF', '2017-10-31'), format='json')

        assert str(orders.json()[0]['SKU']) == 'CHK_LEG_SKIN_OFF'
