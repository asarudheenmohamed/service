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
import json


class TestApiLogin:
    def test_fetch_inventory(self, auth_rest):
        """
        """
        response = auth_rest.get(
            "/inventory/store/",
            {"store_id": 1,
             "website_id": 2},
            format='json')

        assert len(response.json()) > 20

    def test_fetch_inventory_product(self, auth_rest):
        """
        """
        data = {
            "store_id": 1,
            "website_id": 2,
            "product_ids": ",".join(["193", "194"])
        }

        response = auth_rest.get(
            "/inventory/store/",
            data,
            format='json')
        print(response)

        assert len(response.json()) == 2
