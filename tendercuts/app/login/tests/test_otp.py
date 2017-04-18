import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
import uuid
from rest_framework import viewsets, generics, mixins

class TestOtp:
    def test_otp(self, rest):
        response = rest.get("/user/otp/9908765678/", format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

    def test_same_otp(self, rest):
        response = rest.get("/user/otp/9908765678/", format='json')

        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"
        otp = response.data['otp']

        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"
        assert response.data['otp'] == otp