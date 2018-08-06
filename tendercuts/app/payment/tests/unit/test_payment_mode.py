import pytest

from app.payment.lib.gateway.juspay import JuspayPaymentMode


@pytest.mark.django_db
def test_payment_card_add(mock_user, juspay_dummy_card1):
    """Asserts:
        if the card in added to juspay locker
        if the card is deleted from juspay locker
    """

    locker = JuspayPaymentMode()
    customer_id = str(mock_user.entity_id)

    cards = locker.juspay.Cards.list(customer_id="juspay_" + customer_id)
    if cards:
        [locker.juspay.Cards.delete(card_token=card.token) for card in cards]

    before_count = 0

    resp = locker.add_payment_mode(customer_id, juspay_dummy_card1)

    after_count = locker.juspay.Cards.list(customer_id="juspay_" + customer_id)
    assert before_count + 1 == len(after_count)

    # extract token for delete
    juspay_dummy_card1.gateway_code_level_1 = resp.token
    resp = locker.remove_payment_mode(customer_id, juspay_dummy_card1)

    after_count = locker.juspay.Cards.list(customer_id="juspay_" + customer_id)
    assert before_count == len(after_count)
