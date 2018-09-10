import logging

from rest_framework import views, response

from app.core.lib.user_controller import CustomerSearchController
from ..auth import CallCenterAuthentication

logger = logging.getLogger(__name__)


class SearchCustomerApi(views.APIView):
    """Update the customer's lat, lng and geohash details
    """
    authentication_classes = (CallCenterAuthentication,)

    def get(self, request):
        """
        :param request:
            phno: Phone number.

        :return: Response(FlatCustomer)
        """
        phone = self.request.GET['phone']
        customer = CustomerSearchController.load_by_phone_mail(phone)

        return response.Response(customer.deserialize())
