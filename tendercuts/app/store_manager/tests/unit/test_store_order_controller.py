"""Test cases for store order controller."""
import pytest

from app.store_manager.lib.store_order_controller import StoreOrderController


@pytest.mark.django_db
class TestStoreOrderController:
    """Test cases for store order controller."""
    @pytest.mark.parametrize('status, result',
                            [('out_delivery', True),
                            ('canceled', False)])
    def test_store_order(self, mock_user, generate_mock_order, status, result):
        """Fetch all 'out_delivery' and 'complete' state orders.
        Asserts:
            1. check 'out_delivery' and 'complete' state orders are fetched.
        """
        generate_mock_order.status = status
        generate_mock_order.save()

        controller = StoreOrderController()
        sale_order = controller.store_orders(generate_mock_order.store_id)

        obj = sale_order.filter(increment_id=generate_mock_order.increment_id)

        assert obj.exists()  == result
