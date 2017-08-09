"""Login Endpoint."""

import pytest
from django.http import HttpResponseNotFound 

@pytest.mark.django_db
class TestApiLogin:

    def test_endpoint_exists(self, rest):
        response = rest.get("/user/login/", format='json')
        assert not isinstance(response, HttpResponseNotFound)

    def test_user_login(self, rest, mock_user):
        """Login endpoint."""
        response = rest.post(
            "/user/login/",
            {"email": mock_user.email,
             "password": "12345678"
             })

        assert response.data['reward_points'] >= 0
        assert response.data['email'] == mock_user.email
