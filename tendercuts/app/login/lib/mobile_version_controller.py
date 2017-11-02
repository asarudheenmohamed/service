"""Returns assigned driver order obj and driver details based on store id."""
import logging

from django.conf import settings
from distutils.version import StrictVersion
from rest_framework.response import Response


logger = logging.getLogger(__name__)

class MobileVersionControl(object):
    """Mobile version controller."""

    def __init__(self):
        """Constructor."""
        pass

    def version_comparision(self, user_mob_ver):
        """To compare the customer's mobile version.

        Params:
             user_mob_ver:str(customer_mob_ver)

        """
    	MIN_VER = settings.MOBILE_VERSION['min_mobile_version']
    	
    	if StrictVersion(user_mob_ver) > StrictVersion(MIN_VER):
    		update = True
    	else:
    		update = False

    	status = {'upgraded': update, 'mandatory_upgrade': not update}

    	logger.info(
            "Customer's mobile version ({}) updated status is {}".format(
                user_mob_ver, update))

    	return (status) 




