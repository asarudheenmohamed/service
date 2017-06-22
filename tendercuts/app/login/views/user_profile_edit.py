"""API endpoint for change profile details status."""

import logging
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.utils import get_user_id

from ..lib.userprofile_controller import UserProfileEdit

# Get an instance of a logger
logger = logging.getLogger(__name__)


class EditPrifile(APIView):
    """API view to Edit user profile details like email,password, dob,username."""

    def post(self, request, format=None):
        """Return user reset field status.

        Args:
           field(str): user reset field
           value(str):reset value value
        1.reset email,dob,usernmae,password

        Returns:
            user profile changes field value status

        """
        user_id = get_user_id(request)
        field = request.data["field_type"]
        value = request.data["field_value"]

        if field == 'email':
            user_obj = UserProfileEdit(user_id, logger)
            user_obj.reset_email(value)

        elif field == 'password':
            user_obj = UserProfileEdit(user_id, logger)
            user_obj.reset_password(value)

        elif field == 'date of birth':
            user_obj = UserProfileEdit(user_id, logger)
            user_obj.reset_date_of_birth(value)

        else:
            user_obj = UserProfileEdit(user_id, logger)
            user_obj.reset_username(value)

        response = {"status": True,
                    "message": "successfully reset your {}".format(field)}

        return Response(response)
