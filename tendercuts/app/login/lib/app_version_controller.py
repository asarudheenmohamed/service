"""Endpoint to check customer's mobile version."""
import logging
from distutils.version import StrictVersion

from django.conf import settings
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class AppVersionControl(object):
    """Mobile version controller."""

    def __init__(self):
        """Constructor."""
        pass

    def version_comparision(self, user_app_ver):
        """To compare the app version in customer's mobile .

        Params:
         user_app_ver(int): customer app version

        Returns:
            Returns status

        """
        MIN_VER = settings.MOBILE_VERSION['min_app_version']

        if StrictVersion(user_app_ver) > StrictVersion(MIN_VER):
            update = True
        else:
            update = False

        status = {'upgraded': update, 'mandatory_upgrade': not update}

        logger.info(
            "Customer's app version ({}) updated status is {}".format(
                user_app_ver, update))

        return (status)
