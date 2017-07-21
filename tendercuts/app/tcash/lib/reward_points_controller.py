"""Enpoint for the add New user reward amount."""

import logging

from app.core.models.customer.entity import *
from app.core.models.sales_order import *
from app.core.models.store import *


class RewardsPointController:
    """EndPoint add transaction amount for the user."""

    def __init__(self, log=None):
        """Initialize amound value and expired date email sent value."""
        self.log = logging.getLogger('reward_pint')
        self.amount = 50
        self.is_expired = 0
        self.email_sent = 1

    def add_transaction(self, new_user_obj, referrer_obj):
        """Add Transaction amount for new refered user.

        params:
            new_user_obj(obj): request user object
            referrer_obj(obj): referer user objects

        Returns:
            Reward Transaction amount added request user object

        """
        reward_point_obj = MRewardsTransaction(
            customer=new_user_obj.customer, amount=self.amount,
            is_expired=self.is_expired,
            is_expiration_email_sent=self.email_sent,
            comment='{} refer to this customer' .format(
                referrer_obj.customer.entity_id))
        self.log.info("Add reward point amount for the new user  {}".format(
            new_user_obj.customer.entity_id))
        reward_point_obj.save()

        return reward_point_obj
