"""Authentication for driver, only driver will be auth'd."""

import rest_framework.authentication
from rest_framework import exceptions

from app.core.lib.utils import get_mage_userid
from app.driver.constants import DRIVER_GROUP
from app.core.lib.user_controller import CustomerSearchController


class DriverAuthentication(rest_framework.authentication.TokenAuthentication):
    """Driverauthication with group check."""

    def authenticate_credentials(self, key):
        """Override auth and check the customer group.

        @override
        Params:
            key (str): The token Id

        Returns:
            user, token

        """
        user, token = super(DriverAuthentication,
                            self).authenticate_credentials(key)

        mage_id = get_mage_userid(user)
        driver = CustomerSearchController.load_by_id(mage_id)

        if driver.customer.group_id != DRIVER_GROUP:
            raise exceptions.AuthenticationFailed('Invalid token')

        return user, token
