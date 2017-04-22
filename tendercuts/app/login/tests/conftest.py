import pytest
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
import base64
from rest_framework import HTTP_HEADER_ENCODING
import collections


@pytest.fixture
def rest():
    return APIClient()

@pytest.fixture
def mock_user():
    MockUser = collections.namedtuple(
        'MockUser',
        ['username', 'fullname', 'email', 'phone', 'password'],
        verbose=True)

    return MockUser(
        username="mail@varun.xyz",
        fullname="Varun Prasad",
        email="mail@varun.xyz",
        phone="9908765678",
        password="qwerty123")

