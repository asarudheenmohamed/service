from app.payment.lib.gateway import RzpGateway


class TestRzpGateway:
    def test_payment_status(self):
        """
        Asserts:
            if the status returned is true
        """

        vendor_id = "order_7jnpCW8DI9FphH"
        # inc id
        order_id = "400006313"

        gw = RzpGateway()
        status = gw.check_payment_status(order_id, vendor_id)
        assert status == True
