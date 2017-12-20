from .mixin import JuspayMixin

import logging
from app.core.lib.user_controller import CustomerSearchController

class JuspayCustomer(JuspayMixin):
    """Acts as a bridge between tendercuts customer and Juspay"""
    # prefix for juspay users.
    magento_code = "juspay"

    def __init__(self, log=None):
        self.log = log or logging.getLogger()

    @classmethod
    def get_user_id(cls, user_id):
        """Generates the JP user ID from magen"""
        return "{}_{}".format(cls.magento_code, user_id)

    def get_or_create_customer(self, user):
        """Check and create customer if not present.

        params:
            user (str or tuple): Can either be str reprsenting the user id
                or a tuple representing (user_id, mail, phone, name)

        returns:
            juspay.User object

        """
        # conversion to tuple
        if isinstance(user, str) or isinstance(user, unicode):
            user = CustomerSearchController.load_basic_info(str(user))

        user_id = self.get_user_id(user[0])
        self.log.debug("Creating customer in JP with id: {}".format(user_id))

        try:
            cust = self.juspay.Customers.get(id=user_id)
            self.log.debug(
                "Already exist so fetched the customer from JP with id: {}".format(
                    user_id))
        except Exception:
            # this is so wrong, but Jp has no excpetions in theri library
            cust = self.juspay.Customers.create(
                # neeed to be 8 chars
                object_reference_id=user_id,
                email_address=user[1],
                mobile_number=user[2],
                first_name=user[3],
                last_name='')  # last name in mandatory
            self.log.debug(
                "Created a customer in JP with id: {}".format(user_id))

        return cust
