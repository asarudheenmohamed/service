"""
Contains commons fixtures that needs to be shared accorss app
"""
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def rest():
    """Get API client to create requests."""
    return APIClient()


@pytest.fixture(scope="session")
def auth_rest(mock_user):
    """Auth'd Api client to create requests."""
    from django.contrib.auth.models import User
    # A bloody hack to ensure that the user is created in DJ.
    mock_user.generate_token()
    user = User.objects.get(username=mock_user.dj_user_id)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def serializer():
    """Helper class for for resolving API ."""
    class EavSerializer():
        @classmethod
        def serialize(cls, data):
            obj = cls()
            for eav in data:
                print(eav)
                attr_name = eav['code']
                attr_value = eav['value']

                if (type(attr_value) is not list):
                    setattr(obj, attr_name, attr_value)
                else:
                    setattr(
                        obj,
                        attr_name,
                        EavSerializer.serialize(attr_value))
            return obj


@pytest.fixture(scope="module")
def generate_mock_order(request, magento):
    """Generates a mock order.

    Uses pytest caching

    """
    from app.core.lib.test.utils import GenerateOrder
    from app.core.models import SalesFlatOrder
    order_id = request.config.cache.get("mock/order", None)

    if order_id is None:
        order = GenerateOrder().generate_order(18963)
        request.config.cache.set("mock/order", order.increment_id)
    else:
        order = SalesFlatOrder.objects.filter(increment_id=order_id).first()

    return order


@pytest.fixture(scope="session")
def mock_user(request):
    """Generates a mock customer.

    Uses pytest caching

    """
    from app.core.lib.test import generate_customer
    from app.core.lib.user_controller import CustomerSearchController
    from app.core.models.customer import FlatCustomer

    customer_id = request.config.cache.get("mock/customer", None)

    if customer_id is None:
        customer_data = generate_customer()
        customer_id = customer_data['entity_id']
        request.config.cache.set("mock/customer", customer_id)

    customer = CustomerSearchController.load_by_id(customer_id)

    return customer
