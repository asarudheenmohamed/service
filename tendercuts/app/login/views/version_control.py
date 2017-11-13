"""API endpoint to check customer's mobile app version."""

import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from ..lib.app_version_controller import AppVersionControl

logger = logging.getLogger(__name__)


class VersionControl(APIView):
    """Endpoint to check whether customer's app need to upgrade or not.

    EndPoint:
        API: user/version_control/

    """
    def post(self, request, format=None):
        """To check customer's app version to our supported version.

        Input:
            app_verson(str): Customer's mobile app version

        returns:
            Response({upgraded: bool, mandatory_upgrade: bool})

        """
        customer_app_ver = request.data["app_verson"]
        version = AppVersionControl()
        upgrade = version.version_comparision(customer_app_ver)

        logger.info("Customer mobile app version {} was checked".format(
            customer_app_ver))

        return Response(upgrade)
