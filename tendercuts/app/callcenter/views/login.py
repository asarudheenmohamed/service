"""Endpoint for user login."""

import logging
import traceback
import app.core.lib.magento as magento
from app.core.lib.user_controller import CustomerController
from rest_framework.response import Response
from rest_framework.views import APIView
from ..auth import CallCenterPermission
# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserTokenLoginApi(APIView):
    """Enpoint the user deserialized obj."""

    permission_classes = (CallCenterPermission,)

    def post(self, request, format=None):
        """Login endpoint.

        API: callcenter/token_login/

        Params:
            token (str) - user token

        Raises:
            CustomerNotFound

        returns:
            A User object that is serialized
        """
        token = self.request.data['token']

        try:
            user = CustomerController.token_authenticate(token)
            logger.debug(
                "Logging successful for the customer token:{}".format(token))
        except Exception as e:
            user = CustomerController(None)
            user.message = "Invalid username/password"
            exception = traceback.format_exc()

            logger.error("user {} tried to login caused and exception {}".format(
                token,
                exception))
            return Response(user.message)

        return Response(user.deserialize())
