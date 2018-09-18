"""Authentication for user who is auth'd from flock."""
import jwt
import logging
import rest_framework.authentication
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from app.core.models import UserProfile

logger = logging.getLogger()


def verify_token(token):
    """Helper method to validate the token from flock"""
    try:
        resp = jwt.decode(
            token,
            settings.FLOCK_AUTH['APP_SECRET'],
            settings.FLOCK_AUTH['APP_SECRET'])

        return resp
    
    # bad, we just catch any exception and return None
    except Exception:
        return None


class FlockAuthentication(rest_framework.authentication.BaseAuthentication):
    """Storemanagerauthication with group check."""

    def authenticate(self, request):
        """Override auth and check the customer group.

        @override
        Params:
            key (str): Token Id

        Returns:
            user, token

        """
        token = request.data['flockEventToken']

        resp = verify_token(token)

        if resp['appId'] != settings.FLOCK_AUTH['APP_ID']:
            raise AuthenticationFailed(detail="Invalid User")

        parts = resp['userId'].split(":")
        if len(parts) != 2:
            raise AuthenticationFailed(detail="Invalid User")

        user_profile = UserProfile.objects.filter(flock_id=parts[1])

        if not user_profile:
            raise AuthenticationFailed(detail="Invalid User")

        user_profile = user_profile.first()
        user = user_profile.user  # type User
        token = Token.objects.get_or_create(user=user)

        return (user, token)
