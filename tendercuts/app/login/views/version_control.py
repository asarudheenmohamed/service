"""API endpoint to check customer's mobile app version."""

import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from ..lib.app_version_controller import AppVersionControl

logger = logging.getLogger(__name__)


class VersionControl(APIView):
    """Endpoint to check whether customer's app need to upgrade or not.

    EndPoint:
        API: user/version_control/

    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """To check customer's app version to our supported version.

        Input:
            app_verson(str): Customer's mobile app version

        returns:
            Response({upgraded: bool, mandatory_upgrade: bool})

        """
        customer_app_ver = request.data["app_verson"]
        MIN_VER = settings.APP_VERSIONS['CUSTOMER_APP_VERSION']['min_app_version']

        version = AppVersionControl()
        upgrade = version.version_comparision(customer_app_ver, MIN_VER)

        logger.info("Customer mobile app version {} was checked".format(
            customer_app_ver))

        return Response(upgrade)
