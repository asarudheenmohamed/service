"""
Test endpoint "store"
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


@pytest.mark.django_db
class TestApiInventoryFetch(object):
    """Test cases for inventory fetch."""

    def test_fetch_inventory(self, auth_rest):
        """Test case to fetch the inventory.

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.
        """
        response = auth_rest.get(
            "/inventory/store/",
            {"store_id": 1,
             "website_id": 2},
            format='json')

        assert len(response.json()) >= 4

    def test_fetch_inventory_product(self, auth_rest):
        """Test case for fetching inventory with product filter.

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.

        """
        data = {
            "store_id": 1,
            "website_id": 2,
            "product_ids": ",".join(["195", "199"])
        }

        response = auth_rest.get(
            "/inventory/store/",
            data,
            format='json')

        assert len(response.json()) == 2
