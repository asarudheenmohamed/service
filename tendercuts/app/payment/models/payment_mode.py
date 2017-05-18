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
        gateway_code_level_1 (str): More specific code
        priority(int): what should be the priority of these method
    """
    title = models.CharField(max_length=100, blank=False, null=False)
    method = models.CharField(max_length=32, blank=False, null=False)
    gateway_code = models.CharField(max_length=255, blank=False, null=False)

    subtitle = models.CharField(max_length=32, blank=True, null=True)
    gateway_code_level_1 = models.CharField(
        max_length=255, blank=True, null=True)
    priority = models.IntegerField(max_length=255, blank=True, null=True)
    offers = models.CharField(max_length=100, blank=True, null=True)

    # blank true => required
    order_id = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        managed = False

    @classmethod
    def from_justpay(cls, obj):
        """
        Create a payment mode from juspay models

        obj - instance of Payment method or instance of cards
        """

        mode = None

        # Only net banking
        if isinstance(obj, juspay.Payments.PaymentMethod):
            mode = cls(
                title=obj.description,
                method="juspay",  # From settings
                gateway_code=obj.payment_method_type,
                priority=100)
            mode.gateway_code_level_1 = obj.payment_method

        if isinstance(obj, juspay.Cards.Card):
            mode = cls(
                title=obj.number,
                method="juspay",
                gateway_code="CARD",
                priority=101,
            )
            mode.gateway_code_level_1 = obj.token
            mode.subtitle = "{}/{}".format(obj.exp_month, obj.exp_year)

        return mode
