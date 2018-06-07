"""Test the cancel payment pending order task."""

import pytest
from app.payment import tasks
import datetime


@pytest.mark.django_db
def test_cancel_payment_pending_orders(generate_mock_order):
    """Test the cancel payment pending order task.

        Asserts:
         Checks the mock order in cancel order list

    """
    # mock payment pending time
    THRESHOLD = 35 * 60   # 30 mins
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=THRESHOLD)
    generate_mock_order.status = 'pending_payment'
    generate_mock_order.created_at = start
    generate_mock_order.save()

    cancel_orders = tasks.cancel_payment_pending_orders.apply().get()

    assert generate_mock_order in cancel_orders
