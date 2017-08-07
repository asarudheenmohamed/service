from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
import uuid
from django.http.


class TestApiLogin:
    def test_endpoint_exists(self, rest):
        response = rest.get("/user/login/", format='json')
        assert type(response) is not HttpResponseNotFound

    def test_user_login(self, rest, mock_user):
        """DEPRECATED."""
        response = rest.post(
            "/user/login/",
            {"email": mock_user.username,
             "password": mock_user.password})

        print (response.data)
        assert response.data['reward_points'] >= 0
        assert response.data['email'] == mock_user.username
