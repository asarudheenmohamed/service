"""Enpoint for the add new user reward amount status."""
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.utils import get_user_id
from app.tcash.lib.referral_code_controller import ReferralCodeController

logger = logging.getLogger(__name__)


class GetReferralCodeApi(APIView):
    """Get the referral code and text"""

    def get(self, request, format=None):
        user_id = get_user_id(request)
        message = ReferralCodeController(user_id).get_code()

        return Response({
            'status': True,
            'message': message
        })
