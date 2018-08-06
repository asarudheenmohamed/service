from  .mixin import JuspayMixin
from .customer import JuspayCustomer
import logging


class JuspayPaymentMode(JuspayMixin):
    """A wrapper to manage create/delete of payment modes."""
    def __init__(self, log=None):
        self.log = log or logging.getLogger()

    def _create_card(self, user_id, payment_mode):
        """Creates the card in juspay

        :returns (boolean) status
        """
        customer = JuspayCustomer().get_or_create_customer(user_id)
        resp = self.juspay.Cards.create(
            merchant_id=self.merchant_id,
            customer_id=customer.object_reference_id,
            customer_email=customer.email_address,
            card_number=payment_mode.title,
            card_exp_year=payment_mode.expiry_year,
            card_exp_month=payment_mode.expiry_month
        )

        return resp

    def _delete_card(self, user_id, payment_mode):
        """Creates the card in juspay

        :returns (boolean) status
        """
        resp = self.juspay.Cards.delete(
            card_token=payment_mode.gateway_code_level_1)

        return resp

    def add_payment_mode(self, user_id, payment_mode):
        """Add the payment mode to juspay APIs

        :param user_id(str): Magento user id
        :param payment_mode: models.PaymentMode
        :return:
        """
        if payment_mode.is_juspay_card():
            return self._create_card(user_id, payment_mode)

    def remove_payment_mode(self, user_id, payment_mode):
        """Add the payment mode to juspay APIs

        :param user_id(str): Magento user id
        :param payment_mode: models.PaymentMode
        :return:
        """
        if payment_mode.is_juspay_card():
            return self._delete_card(user_id, payment_mode)


