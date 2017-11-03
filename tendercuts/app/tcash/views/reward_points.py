"""Enpoint for the add new user reward amount status."""
import logging
from rest_framework import renderers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.core.models.customer.entity import CustomerEntity, MRewardsReferral
from app.core.models.sales_order import SalesFlatOrder

from ..lib import refer_friend_controller as refer_controller
from ..lib import reward_points_controller as reward_points_controller

logger = logging.getLogger(__name__)


class RewardPointAmountApi(APIView):
    """Enpoint Added amount for refered User."""

    def post(self, request, format=None):
        """Added amount for refered User.

        Params:
            mobile(int):mobile number for referral user

        Returns:
            Added amound for the request user

        """

        refered_user_id = self.request.data['user_id']
        user_id = get_user_id(request)
        user_obj = CustomerSearchController.load_by_id(user_id)
        user_basic_info = CustomerSearchController.load_basic_info(user_id)
        referer_obj = CustomerSearchController.load_by_id(refered_user_id)

        # Fetch existing order of the user
        sales_flat_obj = SalesFlatOrder.objects.values_list(
            'customer_id').filter(customer_id=user_id)
        # Check if the new user id already refered by any other user.
        # as we don't want multiple referrals.
        reward_obj = MRewardsReferral.objects.filter(
            new_customer=CustomerEntity.objects.get(entity_id=user_id))
        if not sales_flat_obj and not reward_obj:
            reward_obj = reward_points_controller.RewardsPointController(
                log=logger)
            reward_point_obj = reward_obj.add_transaction(
                user_obj, referer_obj)
            controller = refer_controller.ReferFriendController(
                log=logger)
            response_data = controller.add_transaction(
                user_obj,
                user_basic_info,
                referer_obj,
                reward_point_obj)
            logger.info("Reward amount added for the user {}".format(
                user_id))
            response_data = {'status': True,
                             'message': "100 Points has been credited to your TCuts Reward account"
                             ".You can use it of further orders."}

        else:
            refered_user_basic_info = CustomerSearchController.load_basic_info(reward_obj[
                0].customer.entity_id)
            response_data = {'status': False,
                             'message': 'Already  you have be referred'
                             ' by your friend {}'.format(refered_user_basic_info[3])}

        return Response(response_data,status=status.HTTP_201_CREATED)
