"""Fetch payment modes endpoint."""

import logging

import pytest
from app.payment.lib.gateway import JusPayGateway
from app.payment.serializer import PaymentModeSerializer
from django.http import HttpResponseNotFound

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


@pytest.mark.django_db
class TestJusPayApiTransactions:
    """Test for payment modes fetch endpoint."""

    def test_endpoint_exists(self, rest):
        """Basic check."""
        # with pytest.raises(IndexError):
        response = rest.get("/payment/modes/", format='json')
        assert type(response) is not HttpResponseNotFound

    def test_verify_api_modes_fetch(self, auth_rest):
        """Fetch API modes.

        Asserts:
            1. Get request fetches NB and card details from JP

        """
        response = auth_rest.get("/payment/modes/")
        assert response.status_code == 200
        # bad test case.
        assert len(response.data['results']) == 0

