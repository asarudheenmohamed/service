# Create your views here.magent
import app.core.lib.magento as magento
from . import lib
from . import models

from rest_framework.response import Response
from rest_framework.views import APIView


class UserLoginApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """

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
