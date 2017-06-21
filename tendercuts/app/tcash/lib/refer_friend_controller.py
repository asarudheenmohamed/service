"""Enpoint for the add new user reward amount status."""
import logging

from app.core.models.customer.entity import *
from app.core.models.sales_order import *
from app.core.models.store import *


class ReferFriendController:
    """EndPoint add transaction amount for the user."""

    def __init__(self, log=None):
        """Get logger name."""
        self.log = log or logging.getLogger()

    def add_transaction(self,
                        user_obj,
                        user_basic_info,
                        referrer_obj,
                        reward_point_obj):
        """Add Transaction amount for new referred user.

        params:  
            user_id(str): request user id
            referrer_obj(obj): referrer user objects

        """
        obj = MRewardsReferral(
            customer=referrer_obj.customer,
            new_customer=user_obj.customer,
            email=user_basic_info[1],
            name=user_basic_info[2], status="visited",
            store=CoreStore.objects.get(store_id=1),
            last_transaction=reward_point_obj)

        self.log.info("Creating Referral object for the new user  {}".format(
            user_basic_info[0]))
        obj.save()

        return obj
        # return {'status': True, 'msg': 'Reward referral amount added '}
