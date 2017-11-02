"""API endpoint to check mobile version."""

import logging
from rest_framework.response import Response
from rest_framework.views import APIView

from ..lib.mobile_version_controller import MobileVersionControl

logger = logging.getLogger(__name__)


class VersionControl(APIView):
    """Endpoint to check whetehr user's mobile need to upgrade or not.

    EndPoint:
        API: user/version_compare/
    
    """
    
    def post(self, request, format=None):
        """To check customer's mobile version to our supported version.

        Input:
            mobile_verson

        returns:
            Response({upgraded: bool, mandatory_upgrade: bool})

        """
        customer_mob_ver = request.data["mobile_verson"]
        version = MobileVersionControl()
        upgrade = version.version_comparision(customer_mob_ver)

        return Response(upgrade)