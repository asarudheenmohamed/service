from app.payment.lib.gateway import GetSimplGateway

class TestSimplTransactionClaim:
    def test_claim(self):
        gw = GetSimplGateway()
        gw.update_order_with_payment(
            "100054118",
            "8be510c41687284f3f70f2e75f92153f")

