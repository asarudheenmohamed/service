"""Enpoint for the add New user reward amount."""

import json
from rest_framework.response import Response
from rest_framework.views import APIView
from ..lib import refer_friend_controller as refer_controller
from app.core.models.store import *
from app.core.models.sales_order import *
from app.core.models.customer.core import *


class RewardPoindAmoundApi(APIView):
    """Enpoint Added amount for refered User."""

    def get_user_id(self):
        """Get User Id.
            
        Returns:
            Get the user id from the request
            username contains u:18963 => 18963 is the magento IDS
        
        """
        user = self.request.user
        user_id = user.username.split(":")

        if len(user_id) < 1:
            user_id = None
        else:
            user_id = user_id[1]

        return user_id

    def dictconvert(self,obj):
        return obj.__dict__

    def post(self, request, format=None):
        """Added amount for refered User.
        
        Params:
            mobile(int):mobile number for referral user
        
        Returns:
            Added amound for the request user
        
        """
        phone = self.request.data['mobile']
        user_id = self.get_user_id()
        user_obj = FlatCustomer.load_by_id(user_id)
        referer_obj = FlatCustomer.load_by_phone_mail(phone)
        user_obj = self.dictconvert(user_obj)
        referer_obj = self.dictconvert(referer_obj)
        sales_flat_obj = SalesFlatOrder.objects.filter(customer_id=user_id)
        reward_obj = MRewardsReferral.objects.filter(
            new_customer=user_obj['customer'], email=user_obj['customer'].email)
        if not sales_flat_obj and not reward_obj:
            controller = refer_controller.ReferFriendController()
            response_data = controller.add_transaction(user_obj, referer_obj)
        else:
            response_data = {'status': 'this is a existing user'}
        data = {"status": response_data['status']}
        return Response(data)
