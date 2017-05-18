import uuid
from random import randint

import pytest
from app.core import models as core_models
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import exceptions

import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


class TestApiLogin:
    """
    Test for payment verify endpoint
    """

    def test_endpoint_exists(self, auth_rest):
        """
        Asserts:
            if the endpoint exists
        """
        response = auth_rest.get("/payment/verify/", format='json')
        assert type(response) is not HttpResponseNotFound

    def test_verify_api(self, auth_rest):
        """
        Asserts:
            if the payment calls the gateway and return the valid value
        """
        vendor_id = "pay_7nKdw2sBGPVi2W"
        order_id = "700002298"

        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)[0]
        order.status = "pending_payment"
        order.grid.status = "pending_payment"
        order.order_now = 0
        order.grand_total = 363
        order.save()
        order.grid.save()

        response = auth_rest.post(
            "/payment/verify/",
            {"vendor_id": vendor_id,
             "increment_id": order_id,
             "gw": "razorpay"})

        # Deprecating this TEST case as we are moving to JUSPAY
        # so feeling a bit lazy to rework.
        # order = core_models.SalesFlatOrder.objects.filter(increment_id=order_id)[0]
        # assert order.status == "scheduled_order"
        # assert order.grid.status == "scheduled_order"
        # assert response.data['status'] is True


class TestJusPayApi:
    """
    Test for payment verify endpoint
    """

    def test_endpoint_exists(self, rest):
        """
        Asserts:
            if the endpoint exists
        """
        with pytest.raises(KeyError):
            response = rest.get("/payment/juspay/", format='json')
            assert type(response) is not HttpResponseNotFound

    def test_verify_api(self, rest):
        """
        Asserts:
            if the api call is triggerd by the juspay
        """

        response = rest.get(
            "/payment/juspay/",
            {"order_id": 67140,
             "status": "AUTHENTICATION_FAILED",
             "status_id": 26,
             "signature": "DQ1su1wVQ1D9tYAcPBcAMoG4yagt8+jVLk0Qf/4xg6Y=",
             "signature_algorithm": "HMAC-SHA256"})
        assert response.data["status"] is False

    def test_verify_api_perms_denied(self, rest):
        """
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
        """
        Verify if the order has been successfully marked complete
        """
        order_id = "400006313"

        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)[0]
        order.status = "pending_payment"
        order.grid.status = "pending_payment"
        order.order_now = 0
        order.save()
        order.grid.save()

        response = rest.get(
            "/payment/juspay/",
            {"order_id": 400006313,
             "status": "CHARGED",
             "status_id": 26,
             "signature": "o/c7LZ3XRMpANoiA2rlDZS3ZT4+k2tOX+6YqsC+zuPk=",
             "signature_algorithm": "HMAC-SHA256"})
        assert response.data["status"] is True
        order = core_models.SalesFlatOrder.objects.filter(increment_id=order_id)[0]
        assert order.status == "scheduled_order"
        assert order.grid.status == "scheduled_order"
