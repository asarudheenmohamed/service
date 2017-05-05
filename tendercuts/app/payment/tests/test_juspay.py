from app.payment.lib.gateway import JusPayGateway


class TestJustPayGateway:
    def test_payment_status(self):
        """
        Asserts:
            if the status returned is true
        """

        # inc id
        order_id = "67126"

        gw = JusPayGateway()
        status = gw.check_payment_status(order_id, None)
        assert status == True
