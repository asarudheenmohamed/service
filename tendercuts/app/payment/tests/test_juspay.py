"""
Verify transaction from juspay
"""

from app.payment.lib.gateway import JusPayGateway, JuspayTransaction
from app.payment.models import PaymentMode
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


class TestJuspayCustomerCreate():
    """
    Test juspy user create
    """

    def test_customer_create(self):
        """
        Test juspy customer create
         Asserts:
            1. user id
            2. phone & mail
        """
        juspay_gw = JusPayGateway()
        cust = juspay_gw.get_or_create_customer("18963")

        assert cust.object_reference_id == "juspay_18963"


class TestJuspayCreateTransaction():
    """
    END to end integration test for creating transaction.
    """
    def _test_create_payment_with_saved_card(self, generate_mock_order, juspay_mock_user):
        """
        Tests create payment with a saved card.

        Asserts:
            1. Transaction create with juspay environment using card that was
               fetched using cards/list (saved card)
        """
        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(juspay_mock_user)

        cards = [m for m in modes if m.gateway_code == "CARD"]
        assert cards[0] is not None
        card = cards[0]

        # set pin and order id
        card.order_id = generate_mock_order.increment_id
        card.pin = "111"

        transaction = gw.start_transaction(card)
        assert transaction.order_id == generate_mock_order.increment_id
        assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url

    def test_create_payment_with_new_card(self, generate_mock_order, juspay_mock_user):
        """
        Fetch a dummy card and mock it into a new card

        Asserts:
            1. Verify if user is created in JP
            2. Verify if order is created in JP
            3. Verify if a token is created for the new card, as we will have no card
            4. Verify if transaction is created for the car
                Standard URL verification
        """
        order_id = generate_mock_order.increment_id
        # set pin & other card details
        card = PaymentMode(
            title="4242424242424242",
            pin="111",
            expiry_year="2020",
            expiry_month="10",
            method="juspay",
            gateway_code="CARD",
            gateway_code_level_1=None,
            order_id=order_id)

        gw = JusPayGateway()
        transaction = gw.start_transaction(card)

        assert juspay.Customers.get(id=juspay_mock_user) is not None

        assert juspay.Orders.status(order_id=order_id) is not None
        assert juspay.Orders.status(order_id=order_id).status == "PENDING_VBV"

        assert "ctkn" in card.gateway_code_level_1

        assert transaction.order_id == generate_mock_order.increment_id
        assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url

    def _test_create_payment_with_nb(self, generate_mock_order):
        """
        Asserts:
            Transaction create in juspay environment using NB
        """
        # create a dummy order
        order_id = generate_mock_order.increment_id

        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)
        # nb1221 JP netbanking pass
        modes[0].order_id = order_id

        with pytest.raises(Exception) as excinfo:
            transaction = gw.start_transaction(modes[0])
            # A stupid way to test because in JP if PG is set up then NB wont
            # work
        assert "Can't find a suitable gateway to process the transaction" in str(
            excinfo.value)

        # assert transaction.order_id == order_id
        # assert "https://sandbox.juspay.in/pay/" in
        # transaction.payment.authentication.url
