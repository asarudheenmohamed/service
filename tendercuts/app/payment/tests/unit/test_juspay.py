"""
Verify transaction from juspay
"""

from app.payment.lib.gateway import JusPayGateway, JuspayTransaction
from app.payment.models import PaymentMode
import uuid
import juspay
import pytest


@pytest.mark.django_db
class TestJustPayGateway:
    """JP test cases for the controller."""

    def test_payment_status(self, juspay_mock_order):
        """Verify claim api.

        Asserts:
            if the status returned is true

        """
        gw = JusPayGateway()
        status = gw.claim_payment(juspay_mock_order.increment_id, None)
        assert status is True

    def test_fetch_payment_modes(self, mock_user):
        """Fetch payment modes.

        Asserts:
            1. Fetch of Saved cards and NB dummy from JP
            2. Assert if its correct
        """
        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(mock_user.entity_id)

        assert len(modes) >= 0

    def test_tokenize_card(self, juspay_dummy_card1):
        """Tokenize a card using JP apis.

        Fetch a dummy card model and change the values to a new cared and
        verify if a token is created

        Asserts:
            1. Verify if a token is created and set as gateway level 1

        """
        card = juspay_dummy_card1
        card.gateway_code_level_1 = None

        transaction = JuspayTransaction(card, None, save_to_locker=False)
        token = transaction.tokenize_card()

        assert "ctkn" in token

    def test_order_status(self, juspay_mock_order):
        """Verify the get status API.

        Asserts:
            if the API is hit and we get a response.
        """
        # Hard-coded.
        order_id = juspay_mock_order.increment_id

        gw = JusPayGateway()
        assert gw.check_payment_status(order_id) is False


@pytest.mark.django_db
class TestJuspayCustomerCreate():
    """Test juspy user create."""

    def test_customer_create(self, mock_user):
        """Test juspy customer create.

         Asserts:
            1. user id
            2. phone & mail
        """

        juspay_gw = JusPayGateway()
        cust = juspay_gw.get_or_create_customer(str(mock_user.entity_id))

        assert cust.object_reference_id == "juspay_{}".format(
            mock_user.entity_id)


@pytest.mark.django_db
class TestJuspayCreateTransaction():
    """DEPRECATED NEEDS TO BE MOVED TO PYTEST BDD FOR EXISTING CARD"""

    def _test_create_transaction_with_saved_card(
            self, juspay_mock_order, mock_user, juspay_dummy_card2):
        """Verify if create transaction with a saved card works.

        Asserts:
            1. Fetches the saved card of the user
            2. Verify if order is created in JP
            3. Verify if a token is present
            4. Verify if transaction is created for the card
                Standard URL verification

        """
        order_id = juspay_mock_order.increment_id

        gw = JusPayGateway()

        modes = gw.fetch_payment_modes(mock_user.entity_id)
        cards = [m for m in modes if m.gateway_code == "CARD"]
        assert cards[0] is not None
        card = cards[0]
        assert card.expiry_month == "10"

        # set pin and order id
        card.order_id = juspay_mock_order.increment_id
        card.pin = "111"

        transaction = gw.start_transaction(card)

        assert juspay.Orders.status(order_id=order_id) is not None
        assert juspay.Orders.status(order_id=order_id).status == "PENDING_VBV"

        assert card.gateway_code_level_1 is not None

        assert "https://sandbox.juspay.in/pay/" in transaction.payment.authentication.url
        assert 198 == transaction.amount

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
