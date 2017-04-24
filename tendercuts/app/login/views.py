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
# import the logging library
import logging
import traceback

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserExistsApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        """
        """
        email = self.request.GET.get('email', None)
        phone = self.request.GET.get('phone', None)


        user_exists = False
        message = ""

        if email and models.FlatCustomer.is_user_exists(email):
            message = "A user with the same email exists, try Forgot password?"
            user_exists = True
            logger.debug("user already exists for the email user {}".format(email))
        elif phone and models.FlatCustomer.is_user_exists(phone):
            message = "A user with the same phone number exists, try Forgot password?"
            user_exists = True
            logger.debug("user already exists for the phone user {}".format(phone))
        elif phone is None and email is None:
            message = "Invalid data"
            user_exists = True
            logger.debug("invalid credentials as both were none")
        else:
            user_exists = False
            message = ""

        # Todo: Optimize and use flat
        return Response({"status": user_exists, "message": message})

class UserLoginApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """
        """
        username = self.request.data.get('email', None) or self.request.data['phone']
        password = self.request.data['password']

        user = None
        try:
            user = models.FlatCustomer.authenticate(
                username, password)
            logger.debug("Logging successful for user {}".format(username))
        except models.CustomerNotFound:
            user = models.FlatCustomer(None)
            user.message = "User does not exists!"
            logger.warn("user {} not found".format(username))
        except models.InvalidCredentials:
            user = models.FlatCustomer(None)
            user.message = "Invalid username/password"
            logger.warn("user {} tried to login with invalid details".format(username))
        except Exception as e:
            user = models.FlatCustomer(None)
            user.message = "Invalid username/password"
            exception = traceback.format_exc()
            logger.error("user {} tried to login caused and exception {}".format(
                username,
                exception))

        # Todo: Optimize and use flat
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
            logger.debug("Got an existing OTP for the number {}".format(otp.mobile))
        except Http404:
            otp = models.OtpList(
                mobile=kwargs['mobile'], otp=random.randint(1000, 9999))
            otp.save()
            logger.debug("Generated a new OTP for the number {}".format(otp.mobile))

        msg = ("""Use {} as your signup OTP. OTP is confidential.""").format(otp.otp)
        SMS().send(phnumber=otp.mobile, message=msg)

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


class UserDataFetch(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """

    def get(self, request, format=None):
        """
        """
        username = self.request.GET.get('email', None) or \
                self.request.GET.get('phone', None)
        fields = ['reward_points', 'store_credit']


        if username is None:
            raise exceptions.ValidationError("Invalid user")

        attributes = []

        try:
            user = models.FlatCustomer.load_by_phone_mail(username)
            logger.debug("Fetched user data {} for {} successfully".format(username, user.__dict__))

            for f in fields:
                attributes.append({
                    "code": f,
                    "value": user._flat[f]
                })

        except Exception as e:
            exception = traceback.format_exc()
            logger.error("user {} tried to fetch data caused and exception {}".format(
                username,
                exception))
            raise exceptions.ValidationError("Invalid user")

        return Response({"attribute": attributes})
