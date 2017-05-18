import logging
import uuid
from random import randint

import pytest
from app.core import models as core_models
from app.payment.lib.gateway import JusPayGateway
from app.payment.serializer import PaymentModeSerializer

from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import exceptions

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


class TestJusPayApi:
    """
    Test for payment modes fetch endpoint
    """

    def test_endpoint_exists(self, rest):
        """
        Asserts:
            if the endpoint exists
        """
        response = rest.get("/payment/modes/", format='json')
        assert type(response) is not HttpResponseNotFound

    def test_verify_api_modes_fetch(self, auth_rest):
        """
        Asserts:
            if the endpoint returns dummy data from user
        """

        response = auth_rest.get("/payment/modes/")
        assert response.status_code == 200
        assert len(response.data['results']) == 1

    def test_api_create_transaction_nb_failure(self, auth_rest):
        """
        Asserts:
            1. POSTING with empty order id throws error
        """

        gateway = JusPayGateway()
        modes = gateway.fetch_payment_modes(16034)
        serialized_data = PaymentModeSerializer(modes[0])

        data = serialized_data.data

        response = auth_rest.post("/payment/modes/", data=data)
        assert response.status_code == 400

    def test_api_create_transaction_nb_sucess(self, auth_rest, juspay_mock_order_id):
        """
        Asserts:
            1. POSTING with empty order id throws error
        """

        gateway = JusPayGateway()
        mode = gateway.fetch_payment_modes(16034)[0]
        mode.order_id = juspay_mock_order_id

        serialized_data = PaymentModeSerializer(mode)
        data = serialized_data.data

        response = auth_rest.post("/payment/modes/", data=data)
        assert response.status_code == 200
        assert "https://sandbox.juspay.in/pay/" in response.data['url']
