"""Test the cancel payment pending order task."""

import pytest
from app.payment import tasks
import datetime
from app.payment.lib.gateway.payu import Payu
import mock


@pytest.mark.django_db
def test_cancel_payment_pending_orders(generate_new_order):
    """Test the cancel payment pending order task.

        Asserts:
         Checks the mock order in cancel order list

    """
    # mock payment pending time
    THRESHOLD = 35 * 60   # 30 mins
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=THRESHOLD)
    payment = generate_new_order.payment.all()[0]
    payment.method = "juspay"
    payment.save()
    generate_new_order.status = 'pending_payment'
    generate_new_order.created_at = start
    generate_new_order.save()

    cancel_orders = tasks.cancel_payment_pending_orders.apply().get()

    assert generate_new_order.increment_id in cancel_orders
