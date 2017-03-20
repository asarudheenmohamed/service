import pytest
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
import base64
from rest_framework import HTTP_HEADER_ENCODING



@pytest.fixture
def rest():
    return APIClient()
