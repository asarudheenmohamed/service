"""Test Test promised delivery time and order count based on test user."""
import json
from datetime import datetime

import dateutil.parser
import pytest
import pytz

from app.core.lib.test.utils import *


@pytest.mark.django_db
class TestOrder:
    """Test promised delivery time and order count."""

    def test_orders(self, auth_rest, mock_user):
        """Test promised delivery time and orders count.

        Params:
        auth_rest(pytest fixture):user requests
        test_user(int):Test user id

        Assers:
         1.Test promised delivery time based on order scheduled slot
         2.Test order fetching count

        """
        sheduled_date = datetime.now()
        sheduled_date.replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
        shedule_date = dateutil.parser.parse(
            "{} {}".format(sheduled_date, "9:00"))

        # 10 order place in mock order
        for i in range(10):
            order_obj = GenerateOrder()
            order_obj = order_obj.generate_order(
                mock_user.entity_id, scheduled_order=True)
        orders = auth_rest.get("/sale_order/orders/?user_id={}".format(
            mock_user.entity_id), format='json')
        print(orders)

        assert str(orders.json()['results'][0]['promised_delivery_time']) == format(
            shedule_date, '%b %d, %a %I:%M %p')

        assert len(orders.data['results']) == 10
