# Create your views here.magent
import app.core.lib.magento as magento
from . import lib
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics, mixins
from app.core.lib.communication import SMS

class UserLoginApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
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


from django.http import Http404
import random
class OtpApiViewSet(
        viewsets.GenericViewSet):
    authentication_classes = ()
    permission_classes = ()

    queryset = models.OtpList.objects.all()
    serializer_class = serializers.OtpSerializer
    lookup_field = "mobile"

    def retrieve(self, request, *args, **kwargs):
        otp = None
        try:
            otp = self.get_object()
        except Http404:
            otp = models.OtpList(mobile=kwargs['mobile'], otp=random.randint(1000, 9999))
            otp.save()
    
        #msg = ("""Use {} as your signup OTP. OTP is confidential.""").format(otp.otp)
        #SMS().send(phnumber=otp.mobile, message=msg)

        serializer = self.get_serializer(otp)
        return Response(serializer.data)