# Create your views here.magent
import app.tcuts.core.magento_api as magento
from rest_framework.views import APIView
from rest_framework.response import Response

class UserLoginApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    def post(self, request, format=None):
        username = self.request.data['username']
        password = self.request.data['password']

        mage = magento.Connector()
        status = mage.api.tendercuts_customer_apis.login(
                username,
                password)

        return Response(status)


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
