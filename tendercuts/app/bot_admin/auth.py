"""Authentication for store manager, only store manager will be auth'd."""
from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user:
            return False

        if not user.is_superuser:
            return False

        return True
