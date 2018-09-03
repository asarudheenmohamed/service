"""Fixtures for driver module."""

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def auth_driver_rest(mock_driver):
    """Auth'd Api client to create requests."""
    from django.contrib.auth.models import User
    # A bloody hack to ensure that the user is created in DJ.
    mock_driver.generate_token()
    user = User.objects.get(username=mock_driver.dj_user_id)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_new_driver_rest(mock_new_driver):
    """Auth'd Api (new version) client to create requests."""
    # A bloody hack to ensure that the user is created in DJ.
    token, created = Token.objects.get_or_create(user=mock_new_driver)

    client = APIClient()
    client.force_authenticate(user=mock_new_driver)
    return client


@pytest.fixture
def django_user(mock_driver):
    django_user = User.objects.get_or_create(
        username=mock_driver.dj_user_id)[0]

    return django_user
