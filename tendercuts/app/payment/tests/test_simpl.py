from app.payment.lib.gateway import GetSimplGateway

class TestSimplTransactionClaim:
    def test_claim(self):
        gw = GetSimplGateway()
        status =  gw.check_payment_status(
            order_id="W800005227",
            #"100054118", 
            vendor_id="8be510c41687284f3f70f2e75f92153f")

        # TODO: fix this shit
        assert status is False
        

