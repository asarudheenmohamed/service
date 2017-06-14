"""Enpoint for the add New user reward amount."""

import logging
from app.core.models.store import *
from app.core.models.customer.entity import *
from app.core.models.sales_order import *


class RewardsPointdController:
    """EndPoint add transection amount for the user."""
    
    def __init__(self):
        """Initialize amound value and expired date email sent value."""
        self.log = logging.getLogger()
        self.amount = 50
        self.is_expired = 365
        self.email_sent = 1

    def add_transaction(self, new_user_obj, referer_obj):
        """Add Transection amount for new refered user.
        
        params:        
            new_user_obj(obj): request user object
            referer_obj(obj): referer user objects
        
        Returns:
            Reward Transection amount added request user object

        """
        reward_point_obj = MRewardsTransaction(
            customer=new_user_obj['customer'], amount=self.amount,
            is_expired=self.is_expired,
            is_expiration_email_sent=self.email_sent,
            comment='%s refer to this customer' % referer_obj['_flat']['firstname'])
        reward_point_obj.save()
        return reward_point_obj
