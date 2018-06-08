"""Test the cancel payment pending order task."""

import pytest
from app.payment import tasks
import datetime
from app.payment.lib.gateway.payu import Payu
import mock


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

    assert generate_mock_order.increment_id in cancel_orders


@pytest.mark.django_db
def test_payubiz_payment_pending_orders(generate_mock_order):
    """Test the payubiz payment pending order task.

        Asserts:
         Checks the mock order state is pending

    """
    # mock payment pending time
    from app.core.models import SalesFlatOrder
    payment = generate_mock_order.payment.all()[0]
    payment.method = "payubiz"
    payment.save()
    THRESHOLD = 35 * 60   # 30 mins
    end = datetime.datetime.now()
    start = end - datetime.timedelta(seconds=THRESHOLD)
    generate_mock_order.status = 'pending_payment'
    generate_mock_order.created_at = start
    generate_mock_order.save()

    with mock.patch.object(Payu, 'check_payment_status',
                           mock.Mock(return_value=True)):
        cancel_orders = tasks.cancel_payment_pending_orders.apply().get()

    order_obj = SalesFlatOrder.objects.filter(
        increment_id=generate_mock_order.increment_id).last()

    assert order_obj.status == 'pending'
