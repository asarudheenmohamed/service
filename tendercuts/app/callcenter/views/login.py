"""Endpoint for user login."""

import logging

import app.core.lib.magento as magento
from app.core.lib.user_controller import CustomerController
from rest_framework.response import Response
from rest_framework.views import APIView

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
        except CustomerNotFound:
            user = CustomerController(None)
            user.message = "User does not exists!"

            logger.warn("user token:{} not found".format(token))

            return Response(user.message)

        return Response(user.deserialize())
