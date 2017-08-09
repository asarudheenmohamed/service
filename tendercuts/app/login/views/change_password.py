"""API endpoint for change password."""
# Create your views here.magent
# import the logging library
import logging

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.user_controller import (CustomerController,
                                          CustomerSearchController)
from app.core.lib.utils import get_user_id

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserChangePassword(APIView):
    """API view to change password.

    1.Ideally this should be part of user
    2.fetch class, since we dont have a serializer yet we will have a different view

    """

    def post(self, request, format=None):
        """Reset password for request user.

        Args:
            request :
                post data:
                1. new_password (str): New password of the user

        Raises:
            exceptions.ValidationError: Raises an exception in
            case not valid user if found

        """
        user_id = get_user_id(request)
        new_password = request.data["new_password"]

        if not user_id:
            raise exceptions.ValidationError("Invalid user")

        user = CustomerSearchController.load_by_id(user_id)

        logger.info("Resetting password for the user {}".format(user_id))
        CustomerController(user.customer).reset_password(new_password)

        return Response({"status": True})
