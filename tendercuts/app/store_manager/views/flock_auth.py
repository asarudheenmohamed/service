"""Endpoint for store manager flock auth."""
import logging

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.auth import FlockAuthentication

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreManagerFlockApi(APIView):
    """Enpoint that logs in user using the data in flock event.

    We first verify if the token is correctly signed, from that we
    do a search of our user profile to find the django user accordingly.
    """

    authentication_classes = (FlockAuthentication,)
    permission_classes = ()

    def post(self, request, format=None):
        """auth endpoint.

        API: store_manager/flock_auth/

        Params:
            flockClient (str) - Type of screen
            flockEventToken (str)- jwt_token
            flockWidgetType(str) - modal, ap
            flockClaimToken(str) - clim
            flockEvent (dict)- name, text, stock, topLevelOrigin, chatName,
                userName, userId

        returns:
            bool

        """
        user = self.request.user
        token = Token.objects.get(user=user)

        return Response({
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'token': token.key,
            'groups': [group.name for group in user.groups.all()]
        })
