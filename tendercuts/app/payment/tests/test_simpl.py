"""
TEst for simple gw
"""
from app.payment.lib.gateway import GetSimplGateway


class TestSimplTransactionClaim:
    """
    Test simple GW
    """
    def test_claim(self):
        """
        Ensure the test transaciotn is claimed
        """
        gw = GetSimplGateway()

        status = gw.claim_payment(
            order_id="W700002925",
            #"100054118",
            vendor_id="8be510c41687284f3f70f2e75f92153f")

        assert status is False
