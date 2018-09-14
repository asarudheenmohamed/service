"""Authentication for user who is auth'd from flock."""
import jwt
import rest_framework.authentication
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from app.core.models import UserProfile


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
        token = Token.objects.get(user=user)

        return user, token
