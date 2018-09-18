"""Authentication for store manager, only store manager will be auth'd."""
import rest_framework.authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions


class StoreManagerAuthentication(rest_framework.authentication.TokenAuthentication):
    """Storemanagerauthication with group check."""

    def authenticate_credentials(self, key):
        """Override auth and check the customer group.

        @override
        Params:
            key (str): Token Id

        Returns:
            user, token

        """
        user, token = super(StoreManagerAuthentication,
                            self).authenticate_credentials(key)

        if not user.groups.filter(name="Store Manager").exists():
            raise AuthenticationFailed(detail="Invalid User")

        return user, token


class StoreManagerPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):

        user = request.user

        if not user:
            return False

        if not user.groups.filter(name="Store Manager").exists():
            return False

        return True

class InventoryManagerPermission(permissions.BasePermission):
    """
    Global permission check for inventory manager.
    """

    def has_permission(self, request, view):

        user = request.user

        if not user:
            return False

        if not user.groups.filter(name="Inventory Manager").exists():
            return False

        return True


