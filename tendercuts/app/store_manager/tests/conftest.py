import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def auth_im(mock_im):
    """Auth'd Api (new version) client to create requests."""
    # A bloody hack to ensure that the user is created in DJ.
    token, created = Token.objects.get_or_create(user=mock_im)

    client = APIClient()
    client.force_authenticate(user=mock_im)
    return client
