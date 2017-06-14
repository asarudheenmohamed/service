"""Enpoint for the add New user reward amount."""
import logging
from app.core.models.store import *
from app.core.models.customer.entity import *
from app.core.models.sales_order import *
from ..lib import reward_points_controller as reward_points_controller


class ReferFriendController:
    """EndPoint add transection amount for the user."""

    def __init__(self):
        """Get logger name."""
        self.log = logging.getLogger()

    def add_transaction(self, user_obj, referer_obj):
        """Add Transection amount for new refered user.
        
        params:        
            user_id(str): request user id
            referer_obj(obj): referer user objects

        """
        reward_obj = reward_points_controller.RewardsPointdController()
        reward_point_obj = reward_obj.add_transaction(
            user_obj, referer_obj)
        obj = MRewardsReferral(
            customer=referer_obj['customer'], new_customer=user_obj['customer'],
            email=user_obj['customer'].email, name=user_obj['_flat']['firstname'], status="visited",
            store=CoreStore.objects.get(store_id=1),
            last_transaction=reward_point_obj)
        obj.save()
        return {'status': 'Reward referral amount added '}
       
