import pytest
from app.payment.lib.gateway import RzpGateway


class TestRzpGateway:
    def test_payment_status(self):
        """
        Asserts:
            if the status returned is true
        """

        vendor_id = "pay_7nKdw2sBGPVi2W"
        # inc id
        order_id = "700002298"

        with pytest.raises(Exception) as excinfo:
            gw = RzpGateway()
            status = gw.claim_payment(order_id, vendor_id)

        assert "captured" in str(excinfo)
