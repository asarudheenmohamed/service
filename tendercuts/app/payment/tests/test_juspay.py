"""
Verify transaction from juspay
"""

from app.payment.lib.gateway import JusPayGateway, JuspayTransaction
import uuid
import juspay
import pytest


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
            1. Fetch of Saved cards and NB dummy from JP
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
            Transaction create in juspay environment using NB
        """
        # create a dummy order
        order_id = juspay_mock_order_id

        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)
        # nb1221 JP netbanking pass
        modes[0].order_id = order_id

        with pytest.raises(Exception) as excinfo:
            transaction = gw.create_payment(modes[0])
            # A stupid way to test because in JP if PG is set up then NB wont
            # work
            assert "Can't find a suitable gateway to process the transaction" in str(
                excinfo.value)

        # assert transaction.order_id == order_id
        # assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url

    def test_create_payment_with_saved_card(self, juspay_mock_order_id):
        """
        Asserts:
            1. Transaction create with juspay environment using card that was
               fetched using cards/list (saved card)
        """
        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)

        cards = [m for m in modes if m.gateway_code == "CARD"]
        assert cards[0] is not None
        card = cards[0]

        # set pin and order id
        card.order_id = juspay_mock_order_id
        card.pin = "111"

        transaction = gw.create_payment(card)
        assert transaction.order_id == juspay_mock_order_id
        assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url

    def test_tokenize_card(self):
        """
        Fetch a dummy card model and change the values to a new cared and
        verify if a token is created

        Asserts:
            1. Verify if a token is created and set as gateway level 1
        """

        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)
        card = [m for m in modes if m.gateway_code == "CARD"][0]
        # set pin
        card.title = "4242424242424242"
        card.pin = "111"
        card.gateway_code_level_1 = None

        transaction = JuspayTransaction(card)
        token = transaction.tokenize_card()

        assert "ctkn" in token

    def test_create_payment_with_new_card(self, juspay_mock_order_id):
        """
        Fetch a dummy card and mock it into a new card

        Asserts:
            1. Verify if a token is created
            2. using that token and the CVV (dummy), a transaction is created
               in JP
            3. Standard URL verification
        """
        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)
        card = [m for m in modes if m.gateway_code == "CARD"][0]
        # set pin & other card details
        card.title = "4242424242424242"
        card.pin = "111"
        card.expiry_year = "2020"
        card.expiry_month = "10"
        card.gateway_code_level_1 = None
        card.order_id = juspay_mock_order_id

        transaction_obj = JuspayTransaction(card)
        transaction = transaction_obj.process()

        assert "ctkn" in transaction_obj.payment_mode.gateway_code_level_1
        assert transaction.order_id == juspay_mock_order_id
        assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url
