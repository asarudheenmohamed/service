"""API endpoint for change profile details status."""

import logging
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.utils import get_user_id

from ..lib.userprofile_controller import UserProfileEdit

# Get an instance of a logger
logger = logging.getLogger(__name__)


class EditProfile(APIView):
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
        value = request.data["field_value"]
        code = request.data["code"]
        if code == 'password_hash':
            user_obj = UserProfileEdit(user_id, logger)
            user_obj.reset_password(code, value)
        else:
            user_obj = UserProfileEdit(user_id, logger)
            user_obj.reset_userprofile(code, value)

        response = {"status": True,
                    "message": "successfully reset your {}".format(code), "result": code}

        return Response(response)
