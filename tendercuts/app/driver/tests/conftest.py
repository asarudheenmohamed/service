import pytest
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
import base64
from rest_framework import HTTP_HEADER_ENCODING



@pytest.fixture
def rest():
    return APIClient()


@pytest.fixture
def username():
    return "9908765678"


@pytest.fixture
def password():
    return "test"


@pytest.fixture
def auth(username, password):
    credentials = ('%s:%s' % (username, password))
    base64_credentials = base64.b64encode(
        credentials.encode(HTTP_HEADER_ENCODING)
    ).decode(HTTP_HEADER_ENCODING)

    auth = 'Basic %s' % base64_credentials

    return auth
