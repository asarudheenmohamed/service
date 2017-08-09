"""Fixtures for driver module."""

import pytest

from app.core.lib.test import generate_customer
from app.core.lib.user_controller import CustomerSearchController


@pytest.fixture(scope="session")
def mock_user(request):
    """Generate a mock customer.

    @override the fixture

    Uses pytest caching.

    """
    customer_id = request.config.cache.get("mock/driver", None)

    if customer_id is None:
        customer_data = generate_customer(group_id=6)
        customer_id = customer_data['entity_id']
        request.config.cache.set("mock/driver", customer_id)

    customer = CustomerSearchController.load_by_id(customer_id)

    return customer
