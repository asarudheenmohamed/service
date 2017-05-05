import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
import uuid

from app.core import models as core_models


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
        vendor_id = "order_7jnpCW8DI9FphH"
        order_id = "400006313"

        order = core_models.SalesFlatOrder.objects.filter(
            increment_id=order_id)[0]
        order.status = "pending_payment"
        order.grid.status = "pending_payment"
        order.order_now = 0
        order.save()
        order.grid.save()

        response = auth_rest.post(
            "/payment/verify/",
            {"vendor_id": vendor_id,
             "increment_id": order_id,
             "gw": "razorpay"})

        order = core_models.SalesFlatOrder.objects.filter(entity_id=1)[0]
        assert order.status == "scheduled_order"
        assert order.grid.status == "scheduled_order"
        assert response.data['status'] is True
