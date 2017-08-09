"""Endpoint for  driver login."""

import logging
import traceback

from rest_framework.response import Response
from rest_framework.views import APIView

from app.core import models
from app.core.lib.user_controller import CustomerController
from app.driver.constants import DRIVER_GROUP

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DriverLoginApi(APIView):
    """
    Enpoint that logs in user.

    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """Login endpoint.

        API: driver/login/

        Params:
            phone (str) - Atleast one of the arguments should
                be provided
            password (str)- Password

        Raises:
            InvalidCredentials
            Exception in case of any other issues.

        returns:
            A User object that is serialized
        """
        username = self.request.data['phone']
        password = self.request.data['password']

        user = None
        try:
            user = CustomerController.authenticate(username, password)

            # Hack: Refactor code after azhars revamp
            if user.customer.group_id != DRIVER_GROUP:
                raise Exception("Inalid username/password")

            logger.debug("Logging successful for driver {}".format(username))
        except Exception as exception:
            user = models.FlatCustomer(None)
            user.message = "Invalid username/password"
            exception = traceback.format_exc()
            logger.error("user {} tried to login caused and exception {}".format(
                username,
                exception))

        # Todo: Optimize and use flat
        return Response(user.deserialize())
