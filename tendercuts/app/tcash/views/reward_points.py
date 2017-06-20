"""Enpoint for the add new user reward amount status."""
import logging
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from ..lib import refer_friend_controller as refer_controller
from app.core.models.store import *
from app.core.models.sales_order import *
from app.core.models.customer.core import *
from ..lib import reward_points_controller as reward_points_controller
from app.core.lib.test.utils import *

logger = logging.getLogger(__name__)


class RewardPointAmoundApi(APIView, GetUser):
    """Enpoint Added amount for refered User."""

    def post(self, request, format=None):
        """Added amount for refered User.

        Params:
            mobile(int):mobile number for referral user

        Returns:
            Added amound for the request user

        """

        phone = self.request.data['user_id']
        user_id = GetUser.__init__(self)
        user_obj = FlatCustomer.load_by_id(user_id)
        user_basic_info = FlatCustomer.load_basic_info(user_id)
        referer_obj = FlatCustomer.load_by_id(phone)

        sales_flat_obj = SalesFlatOrder.objects.values_list('customer_id').filter(
            customer_id=user_basic_info[0])
        reward_obj = MRewardsReferral.objects.filter(
            new_customer__entity_id=user_basic_info[0])

        if not sales_flat_obj and not reward_obj:
            print 'asar'
            reward_obj = reward_points_controller.RewardsPointdController(
                log=logger)
            reward_point_obj = reward_obj.add_transection(
            user_obj, referer_obj)
            controller = refer_controller.ReferFriendController(
                log=logger)
            response_data = controller.add_transection(
                user_obj,
                user_basic_info,
                referer_obj,
                reward_point_obj)
            logger.info("Reward amount added for the user {}".format(
                user_basic_info[0]))
        else:
            response_data = {'status': False, 'msg': 'this is a existing user'}

        return Response(response_data)
