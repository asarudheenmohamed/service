import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
import uuid
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
import base64
from rest_framework import HTTP_HEADER_ENCODING
import collections

@pytest.fixture
def rest():
    return APIClient()

class TestApiLogin:
    def test_add_to_cart(self, rest):
        """
        """
        response = rest.post(
                "/core/cart/add/",
                {"product_id": 192,
                 "quantity": 1},
                format='json')

        assert response.data['status'] is True


