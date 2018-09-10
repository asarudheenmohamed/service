"""Authentication for driver, only driver will be auth'd."""

import rest_framework.authentication
from rest_framework import exceptions
from rest_framework import permissions


class CallCenterAuthentication(rest_framework.authentication.TokenAuthentication):
    """Call center with group check."""

    def authenticate_credentials(self, key):
        """Override auth and check the customer group.

        @override
        Params:
            key (str): The token Id

        Returns:
            user, token

        """
        user, token = super(CallCenterAuthentication,
                            self).authenticate_credentials(key)

        if not user.groups.filter(name="Call Center").exists():
            raise exceptions.AuthenticationFailed(detail="Invalid User")

        return user, token

class CallCenterPermission(permissions.BasePermission):
    """
    Global permission check for callcenter group.
    """

    def has_permission(self, request, view):

        user = request.user

        if not user:
            return False

        if not user.groups.filter(name="Call Center").exists():
            return False

        return True

