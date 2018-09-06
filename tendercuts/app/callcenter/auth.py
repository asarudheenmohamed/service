"""Authentication for driver, only driver will be auth'd."""

import rest_framework.authentication
from rest_framework import exceptions


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
