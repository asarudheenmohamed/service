"""
Contains commons fixtures that needs to be shared accorss app
"""
import pytest
from rest_framework.test import APIClient
from app.core.lib.test.test_utils_order_placed import *

@pytest.fixture
def rest():
    return APIClient()


@pytest.fixture
def auth_rest():
    from django.contrib.auth.models import User
    user = User.objects.get(username="u:18963")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def serializer():
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

@pytest.fixture(scope="session")
def generate_mock_order(magento):
    return GenerateOrder(18963).order
