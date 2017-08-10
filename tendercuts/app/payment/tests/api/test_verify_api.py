"""Test cases for juspay payment"""

import logging

import pytest
from django.http import HttpResponseNotFound, HttpResponseRedirect

from app.core import models as core_models

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


@pytest.mark.django_db
class TestJusPayApi:
    """Test for payment verify endpoint."""

    def test_endpoint_exists(self, rest):
        """Verify endpoint exists."""
        with pytest.raises(KeyError):
            response = rest.get("/payment/juspay/", format='json')
            assert type(response) is not HttpResponseNotFound

    def test_verify_api(self, rest):
        """Success case.

        Asserts:
            if the api call is triggerd by the juspay
            And redirect is triggered

        """
        response = rest.get(
            "/payment/juspay/",
            {"order_id": 67140,
             "status": "AUTHENTICATION_FAILED",
             "status_id": 26,
             "signature": "DQ1su1wVQ1D9tYAcPBcAMoG4yagt8+jVLk0Qf/4xg6Y=",
             "signature_algorithm": "HMAC-SHA256"})
        assert type(response) is HttpResponseRedirect

    def test_verify_api_perms_denied(self, rest):
        """Failure case, where call is not triggered by juspay.

        Asserts:
            if the api call is not triggerd by juspay

        """
        response = rest.get(
            "/payment/juspay/",
            {"order_id": 67140,
             "status": "AUTHENTICATION_FAILED",
             "status_id": 26,
             "signature": "DQ1su1wVQ1D9tYAcPBcAMoG4ygt8+jVLk0Qf/4xg6Y=",
             "signature_algorithm": "HMAC-SHA256"})
        assert response.status_code == 403

    def test_order_success(self, rest):
        """Success case.

        Verify if the order has been successfully marked complete

        Asserts:
            1. Get Request to the API set the order status to sc.order or pending
            from payment pending

        """
        order_id = "400006313"

        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id).first()
        order.status = "pending_payment"
        order.grid.status = "pending_payment"
        order.order_now = 0
        order.save()
        order.grid.save()

        response = rest.get(
            "/payment/juspay/",
            {"order_id": order_id,
             "status": "CHARGED",
             "status_id": 26,
             "signature": "o/c7LZ3XRMpANoiA2rlDZS3ZT4+k2tOX+6YqsC+zuPk=",
             "signature_algorithm": "HMAC-SHA256"})
        # assert response.data["status"] is True
        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id).first()
        assert order.status == "pending"
        assert order.grid.status == "pending"
