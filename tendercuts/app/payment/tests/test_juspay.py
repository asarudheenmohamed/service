"""
Verify transaction from juspay
"""

from app.payment.lib.gateway import JusPayGateway
import uuid
import juspay


class TestJustPayGateway:
    """
    JP test cases
    """

    def test_payment_status(self):
        """
        Asserts:
            if the status returned is true
        """

        # inc id
        order_id = "100000001"

        gw = JusPayGateway()
        status = gw.check_payment_status(order_id, None)
        assert status == True

    def test_verify(self):
        """
        Asserts:
            The transaction callback from juspay

        """

        # Test via the APIs
        pass

    def test_fetch_payment_modes(self):
        """
        Asserts:
            Fetch of payment modes and NB dummy is present
        """
        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)

        assert len(modes) == 2

        nb = [mode for mode in modes if mode.gateway_code == "NB"][0]
        cards = [mode for mode in modes if mode.gateway_code == "CARD"]

        assert nb.title == "Dummy Bank"
        assert nb.gateway_code_level_1 == "NB_DUMMY"
        assert nb.gateway_code == "NB"

        # cards
        assert cards[0].title == "4242-XXXXXXXX-4242"
        assert cards[0].title == "4242-XXXXXXXX-4242"
        assert cards[0].method == "juspay"
        assert cards[0].gateway_code == "CARD"
        assert cards[0].gateway_code_level_1 != None

    def test_create_payment_with_nb(self, juspay_mock_order_id):
        """
        Asserts:
            Transaction create in juspay environment
        """
        # create a dummy order
        order_id = juspay_mock_order_id

        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)
        # nb1221 JP netbanking pass
        modes[0].order_id = order_id
        transaction = gw.create_payment(modes[0])

        assert transaction.order_id == order_id
        assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url
