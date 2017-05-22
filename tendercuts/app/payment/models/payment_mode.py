"""
Transient model for payment modes
"""
from django.db import models
import juspay


class PaymentMode(models.Model):
    """
    params:
        title (str): Main display title
        subtitle: Card expiry etc
        offers : Offers string if any
        method (str): Main payment mode name (juspay, simpl), should corerspond
            to magento
        gateway_code (str): Gateway specific name, such as "NB", CARDS etc
        gateway_code_level_1 (str): More specific code of the GW vendor [TOKEN, NB CODE]etc
        priority(int): what should be the priority of these method
        order_id(str): Id of the order from magento
        pin (str): Can be a password/pin/cvv
        expiry_month (str): MM format
        expiry_year (str): YYYY format
    """
    title = models.CharField(max_length=100, blank=False, null=False)
    subtitle = models.CharField(max_length=32, blank=True, null=True)

    method = models.CharField(max_length=32, blank=False, null=False)
    gateway_code = models.CharField(max_length=255, blank=False, null=False)
    gateway_code_level_1 = models.CharField(
        max_length=255, blank=True, null=True)

    priority = models.IntegerField(blank=True, null=True)
    offers = models.CharField(max_length=100, blank=True, null=True)

    # blank true => required
    order_id = models.CharField(max_length=100, null=False, blank=False)

    # Card specifid
    pin = models.CharField(max_length=32, blank=True, null=True)
    expiry_month = models.CharField(max_length=32, blank=True, null=True)
    expiry_year = models.CharField(max_length=32, blank=True, null=True)
    # MC/VISA
    brand = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False

    @classmethod
    def from_justpay(cls, obj):
        """
        Create a payment mode from juspay models

        obj - instance of Payment method or instance of cards
        """
        TOP_NBS = ["NB_HDFC", "NB_ICICI", "NB_SBI", "NB_AXIS", "NB_KOTAK"]

        mode = None

        # Only net banking
        if isinstance(obj, juspay.Payments.PaymentMethod):

            try:
                priority = TOP_NBS.index(obj.payment_method)
            except ValueError:
                priority = 100

            mode = cls(
                title=obj.description,
                method="juspay",  # From settings
                gateway_code=obj.payment_method_type,
                priority=priority)

            # eg: NB_HDFC
            mode.gateway_code_level_1 = obj.payment_method
            # NB, HDFC
            comps = obj.payment_method.split("_")
            mode.subtitle = ""
            if len(comps) > 1:
                mode.subtitle = comps[1]

        # Brand
        if isinstance(obj, juspay.Cards.Card):
            mode = cls(
                title=obj.number,
                method="juspay",
                gateway_code="CARD",
                priority=101,
            )
            mode.gateway_code_level_1 = obj.token
            mode.subtitle = "{}/{}".format(obj.exp_month, obj.exp_year)
            mode.expiry_month = obj.exp_month
            mode.expiry_year = obj.exp_year
            mode.brand = obj.brand

        return mode

    def is_juspay_card(self, new_check=False):
        """
        check if the payment method is juspay card

        params:
            new_check: if set checks if its a new card using the token param

        returns:
            boolean
        """
        is_card = self.method == "juspay" and self.gateway_code == "CARD"

        # if not a store card
        if new_check:
            is_card = is_card and self.gateway_code_level_1 is None

        return is_card

    def is_juspay_nb(self):
        """
        check if the payment method is juspay NB

        return:
            boolean True if nb otherwise false
        """
        return self.method == "juspay" and self.gateway_code == "NB"
