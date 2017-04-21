# Create your views here.magent
import redis
import app.core.lib.magento as magento
from . import lib
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics, mixins, exceptions
from app.core.lib.communication import SMS
from django.http import Http404
import random
import string


class UserLoginApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """
        """
        username = self.request.data['email'] or self.request.data['phone']
        password = self.request.data['password']

        user = None
        try:
            user = models.FlatCustomer.authenticate(
                username, password)
        except models.CustomerNotFound:
            user = models.FlatCustomer(None)
            user.message = "User does not exists!"
        except models.InvalidCredentials:
            user = models.FlatCustomer(None)
            user.message = "Invalid username/password"
        except Exception:
            user = models.FlatCustomer(None)
            user.message = "Invalid username/password"

        return Response(user.deserialize())


class UserSignUpApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """

    def post(self, request, format=None):
        """
        """
        email = self.request.data['email']
        phone = self.request.data['phone']
        password = self.request.data['password']
        fullname = self.request.data['name']

        mage = magento.Connector()
        status = mage.api.tendercuts_customer_apis.signup(
            fullname,
            email,
            phone,
            password)

        return Response(status)


class OtpApiViewSet(viewsets.GenericViewSet):
    """
    """
    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        """
        """
        otp = None
        try:
            otp = self.get_object()
        except Http404:
            otp = models.OtpList(
                mobile=kwargs['mobile'], otp=random.randint(1000, 9999))
            otp.save()

        #msg = ("""Use {} as your signup OTP. OTP is confidential.""").format(otp.otp)
        #SMS().send(phnumber=otp.mobile, message=msg)

        serializer = self.get_serializer(otp)
        return Response(serializer.data)


class OtpForgotPasswordApiViewSet(viewsets.GenericViewSet):
    """
    OTP for resetting password
    TODO: EXTREMELY HACKY
    """
    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        """
        """
        redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

        phone = kwargs['mobile']
        # check if user exists
        customer = models.FlatCustomer.load_by_phone_mail(phone)

        otp = models.OtpList.redis_get(redis_db, phone)

        if otp is None:
            otp = models.OtpList(
                mobile=phone,
                otp=random.randint(1000, 9999))
            models.OtpList.redis_save(redis_db, otp)

        msg = ("""Use {} as your OTP to reset your password.""").format(otp.otp)
        SMS().send(phnumber=otp.mobile, message=msg)

        otp.otp = None
        serializer = self.get_serializer(otp)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

        phone = self.request.data['mobile']
        otp = self.request.data['otp']
        dry_run = self.request.data.get('dry_run', False)

        otp_object = models.OtpList.redis_get(redis_db, phone)

        if otp_object is None or otp_object.otp != otp:
            raise exceptions.ValidationError("Invalid OTP")

        random_pass = ''.join(
            [random.choice(string.ascii_lowercase) for n in xrange(5)])
        random_pass += str(random.randint(0, 9))

        msg = ("""Your request for password reset is now successful. New password: {}""").format(
            random_pass)
        SMS().send(phnumber=phone, message=msg)

        customer = models.FlatCustomer.load_by_phone_mail(phone)
        customer.reset_password(random_pass, dry_run=dry_run)

        otp_object.otp = None
        serializer = self.get_serializer(otp_object)
        return Response(serializer.data)
