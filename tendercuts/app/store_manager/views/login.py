"""Endpoint for store manager login."""

import logging
import traceback

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreManagerLoginApi(APIView):
    """
    Enpoint that logs in user.

    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """Login endpoint.

        API: store_manager/login/

        Params:
            email (str) - Atleast one of the arguments should
                be provided
            password (str)- Password

        Raises:
            InvalidCredentials
            Exception in case of any other issues.

        returns:
            A User object that is serialized
        """
        username = self.request.data['email']
        password = self.request.data['password']

        user = User.objects.get(username=username)
        if not user:
            raise AuthenticationFailed(detail="Invalid User")

        if user.check_password(password):
            raise AuthenticationFailed(detail="Invalid User")

        if not user.groups.filter(name="Store Manager").exists():
            raise AuthenticationFailed(detail="Invalid User")

        token, created = Token.objects.get_or_create(user=user)
        logger.debug("Logging successful for SM {}".format(user.email))

        # Todo: Optimize and use flat
        return Response({
            'username': user.username,
            'email': user.email,
            'token': token.key
        })
