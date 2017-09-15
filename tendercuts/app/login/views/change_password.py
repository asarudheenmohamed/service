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
        """If the user reset the password means that will set as a new password.

        otherwise it automatically generate the password and send to the user via sms.

        Params:
            new_password (str): New password of the user
            mobile(int): customer mobile number

        Raises:
            exceptions.ValidationError: Raises an exception in
            case not valid user if found

        """

        mobile = self.request.data.get('mobile', False)
        new_password = self.request.data.get('new_password', False)

        user_id = get_user_id(request)

        if not user_id:
            raise exceptions.ValidationError("Invalid user")

        user = CustomerSearchController.load_by_id(user_id)

        logger.info("Resetting password for the user {}".format(user_id))
        controller = CustomerController(user.customer)

        if not new_password:
            logger.info(
                "Generate password and then reset.for the user {}".format(user_id))
            controller.generate_and_reset_password(mobile)
        else:
            controller.reset_password(new_password)
        logger.info(
            "Successfully password reset.for the user {}".format(user_id))

        return Response({"status": True})
