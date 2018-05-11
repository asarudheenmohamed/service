"""Fixtures for driver module."""

import pytest
from rest_framework.test import APIClient

from app.core.lib.test import generate_customer
from app.core.lib.user_controller import CustomerSearchController
from app.driver.constants import DRIVER_GROUP
from django.contrib.auth.models import User


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
def django_user(mock_driver):
    django_user = User.objects.get_or_create(
        username=mock_driver.dj_user_id)[0]

    return django_user
