import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from random import randint
import uuid
import redis
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


class TestPasswordRestOtp:
    def test_otp(self, rest):
        
        response = rest.get("/user/forgot_password_otp/9908765678/", format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"
        
        redis_conn = redis.StrictRedis(host="localhost", port=6379, db=0)
        otp = redis_conn.get("{}:{}".format("FORGOT_OTP", "9908765678"))

        response = rest.get("/user/forgot_password_otp/9908765678/", format='json')
        assert response.data['mobile'] == "9908765678"
        otp1 = redis_conn.get("{}:{}".format("FORGOT_OTP", "9908765678"))
        assert otp == otp1
    
    def test_raise_error(self, rest):
        with pytest.raises(Exception):
            response = rest.get("/user/forgot_password_otp/9908765678111/", format='json')
    

    def test_otp_password_reset(self, rest):
        response = rest.get("/user/forgot_password_otp/9908765678/", format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"
        
        redis_conn = redis.StrictRedis(host="localhost", port=6379, db=0)
        otp = redis_conn.get("{}:{}".format("FORGOT_OTP", "9908765678"))

        data = {"mobile": "9908765678", "otp": otp, "dry_run": True}
        response = rest.post("/user/forgot_password_otp/", data, format='json')
        assert type(response) is not None
        assert response.data['mobile'] == "9908765678"

