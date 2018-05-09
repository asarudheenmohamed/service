from app.core import models as core_models
from app.payment.lib.gateway.juspay import JuspayOrderSuccessProcessor
from app.driver import tasks

import pytest
import uuid
import mock

@pytest.fixture
def mock_order():
    order = {
        "increment_id": str(uuid.uuid4()).replace("-", ""),
        "total_item_count": 5,
        "rewardpoints_earn": 0,
        "rewardpoints_spent": 0,
        "rewardpoints_base_discount": 0,
        "rewardpoints_discount": 0,
        "rewardpoints_base_amount": 0,
        "rewardpoints_amount": 0,
        "rewardpoints_referal_earn": 0,
        "rewardpoints_invited_discount":0,
        "rewardpoints_invited_base_discount": 0,
        "rewardpoints_refer_customer_id": 0,
        "location_id": 0,
        "mail_send":0,
        "order_now": 1,
        "driver_id": 0
    }

    order = core_models.SalesFlatOrder.objects.create(**order)
    payment = core_models.SalesFlatOrderPayment.objects.create(
        parent=order, method="cashondelivery")

    return order

class TestWebhook:

    @pytest.mark.parametrize("initial_state,expected_state,initial_payment_mode,should_call", [
        ("pending_payment", "pending", "cashondelivery", True),
        ("out_delivery", "out_delivery", "cashondelivery", True),
        ("processing", "processing", "cashondelivery", True),
        ("pending", "pending", "juspay", False),
        ("scheduled_order", "scheduled_order", "juspay", False)
    ])
    @pytest.mark.django_db
    def test_order_confirmation(self, mock_order, initial_state,
        expected_state, initial_payment_mode, should_call):
        """Asserts:
        1\ Status change
        2\ payment mode change.
        """

        mock_order.status = initial_state
        mock_order.save()

        payment = core_models.SalesFlatOrderPayment.objects.filter(
            parent=mock_order).first()
        payment.method = initial_payment_mode
        payment.save()

        payload = {
            'event_name': u'ORDER_SUCCEEDED',
            'content': {
                'order': {
                    'order_id': mock_order.increment_id,
                    'payment_method': u'VISA'
                }
            }
        }

        with mock.patch.object(tasks.send_sms, 'delay', mock.Mock(return_value=1)) as mock_method:
            processor = JuspayOrderSuccessProcessor.from_payload(payload)
            processor.execute()
            if should_call:
                mock_method.assert_called()
            else:
                mock_method.assert_not_called()

        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=mock_order.increment_id).first()
        assert order.status == expected_state
        assert order.payment.all()[0].method == "juspay"
