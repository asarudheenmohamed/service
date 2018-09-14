"""Endpoint for store manager flock auth."""
import logging
import jwt

from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.models import UserProfile

# Get an instance of a logger
logger = logging.getLogger(__name__)


class StoreManagerFlockApi(APIView):
    """Enpoint that logs in user."""

    authentication_classes = ()
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
        token = self.request.data['flockEventToken']

        resp = jwt.decode(
            token,
            settings.FLOCK_AUTH['APP_SECRET'],
            settings.FLOCK_AUTH['APP_SECRET'])

        if resp['appId'] != settings.FLOCK_AUTH['APP_ID']:
            raise AuthenticationFailed(detail="Invalid User")

        user_profile = UserProfile.objects.filter(flock_id=resp['userId'])

        if not user_profile:
            raise AuthenticationFailed(detail="Invalid User")

        user_profile = user_profile.first()
        user = user_profile.user  # type User
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'token': token.key,
            'groups': [group.name for group in user.groups.all()]
        })
