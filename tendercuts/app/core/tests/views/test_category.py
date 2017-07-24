"""
Test endpoint "product"
"""

import base64
import collections
import json
import uuid
from random import randint

import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from requests.auth import HTTPBasicAuth
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.test import APIClient


class TestApiInventoryFetch(object):
    """Test cases for products fetch."""

    def test_fetch_product(self, auth_rest):
        """Test case to fetch the products.

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.
            2. If the first category is what;s new
        """
        response = auth_rest.get(
            "/core/product/",
            {"store_id": 1},
            format='json')

        assert len(response.data) >= 6
        assert "New" in response.data[0]['category']['name']
