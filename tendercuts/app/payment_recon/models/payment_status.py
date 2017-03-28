from __future__ import unicode_literals
from django.db import models

# export models that are used
from app.core.models import SalesFlatOrder


class PaymentStatusResponse(models.Model):
    tpn = models.CharField(max_length=200)
    vendor_name = models.CharField(max_length=200)
    vendor_id = models.CharField(max_length=200)
    vendor_status = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    # Tendercuts custom status
    is_payment_captured = models.BooleanField()
    amount_captured = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)

    @property
    def order(self):
        return SalesFlatOrder.objects.filter(increment_id=self.tpn)


    @classmethod
    def from_payu_status(cls, order, status_dict):

        vendor_id = status_dict['mihpayid']
        # Get the status, if present
        status = status_dict.get('status', "NA")
        # Cancel the order only when the status is failure
        # so send payment capture to false accordingly
        is_payment_captured = not (status == "failure")

        amount_captured = status_dict.get("net_amount_debit", "-1")

        return cls(
                tpn=order.increment_id,
                vendor_name="payu",
                vendor_id=vendor_id,
                vendor_status=status,
                is_payment_captured=is_payment_captured,
                amount_captured=amount_captured)

