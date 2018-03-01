"""Authentication for store manager, only store manager will be auth'd."""

import rest_framework.authentication

class StoreManagerAuthentication(rest_framework.authentication.TokenAuthentication):
    """Storemanagerauthication with group check."""

    def authenticate_credentials(self, key):
        """Override auth and check the customer group.

        @override
        Params:
            key (str): Token Id

        Returns:
            user, token

        """
        user, token = super(StoreManagerAuthentication,
                            self).authenticate_credentials(key)

        if not user.groups.filter(name="Store Manager").exists():
            import pdb
            pdb.set_trace()
            raise AuthenticationFailed(detail="Invalid User")

        # mage_id = get_mage_userid(user)
        # driver = CustomerSearchController.load_by_id(mage_id)

        # if driver.customer.group_id != DRIVER_GROUP:
        #     raise exceptions.AuthenticationFailed('Invalid token')
        
        return user, token
