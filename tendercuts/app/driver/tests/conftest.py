"""Fixtures for driver module."""

import pytest
from rest_framework.test import APIClient

from app.core.lib.test import generate_customer
from app.core.lib.user_controller import CustomerSearchController
from app.driver.constants import DRIVER_GROUP
from django.contrib.auth.models import User


@pytest.fixture(scope="session")
def mock_driver(request):
    """Generate a mock customer.

    @override the fixture

    Uses pytest caching.

    """
    customer_id = request.config.cache.get("mock/driver", None)
    if customer_id is None:
        customer_data = generate_customer(group_id=DRIVER_GROUP)
        customer_id = customer_data['entity_id']
        request.config.cache.set("mock/driver", customer_id)

    customer = CustomerSearchController.load_by_id(customer_id)

    return customer


@pytest.fixture(scope="session")
def auth_driver_rest(mock_driver):
    """Auth'd Api client to create requests."""
    from django.contrib.auth.models import User
    # A bloody hack to ensure that the user is created in DJ.
    mock_driver.generate_token()
    user = User.objects.get(username=mock_driver.dj_user_id)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture(scope="session")
def django_user(mock_driver):
    django_user = User.objects.get(username=mock_driver.dj_user_id)

    return django_user
