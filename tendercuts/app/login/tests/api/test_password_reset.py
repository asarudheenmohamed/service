import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
from rest_framework.test import APIClient
import uuid
import redis
from rest_framework import viewsets, generics, mixins


class TestChangePassword:
    def test_change_password(self, auth_rest):
        response = auth_rest.post(
            "/user/change_password/",
            data={"new_password": "qwerty123"},
            format='json')
        assert type(response) is not None
        assert response.data['status'] is True

