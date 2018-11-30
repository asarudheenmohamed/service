
"""Verify transaction from juspay."""


import pytest
from app.payment.lib.gateway import JusPayGateway
from app.payment.serializer import PaymentModeSerializer


@pytest.mark.django_db
class TestSerializer:
    """
    Dummy test for serilaizer
    """

    def test_serializer(self):
        """
        Test if serialization is happenign
        """
        gw = JusPayGateway()
        modes = gw.fetch_payment_modes(16034)
        data = PaymentModeSerializer(modes, many=True)
        assert data is not None
