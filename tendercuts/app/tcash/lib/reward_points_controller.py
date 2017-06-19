"""Enpoint for the add New user reward amount."""

import logging
from app.core.models.store import *
from app.core.models.customer.entity import *
from app.core.models.sales_order import *


class RewardsPointdController:
    """EndPoint add transection amount for the user."""

    def __init__(self, log=None):
        """Initialize amound value and expired date email sent value."""
        self.log = log or logging.getLogger()
        self.amount = 50
        self.is_expired = 0
        self.email_sent = 1

    def add_transection(self, new_user_obj, referer_obj):
        """Add Transection amount for new refered user.

        params:
            new_user_obj(obj): request user object
            referer_obj(obj): referer user objects

        Returns:
            Reward Transection amount added request user object

        """
        reward_point_obj = MRewardsTransaction(
            customer=new_user_obj.customer, amount=self.amount,
            is_expired=self.is_expired,
            is_expiration_email_sent=self.email_sent,
            comment='{} refer to this customer' .format(
                referer_obj.customer.entity_id))
        self.log.info("Add reward point amount for the new user  {}".format(
                new_user_obj.customer.entity_id))
        reward_point_obj.save()

        return reward_point_obj
