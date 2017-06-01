"""Summary

Attributes:
    logger (TYPE): Description
"""
# Create your views here.magent
# import the logging library
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from app.core.models.customer.entity import MRewardsTransaction
from django.http import HttpResponse, JsonResponse
from app.login.views.serializers import RewardPointSerializer
"""
Endpoint for  user login
"""

from .. import serializers

logger = logging.getLogger(__name__)
# Get an instance of a logger

class RewardPointsTransection(APIView):
    """
    user/fetch : Gets the user Reward point transection data
    """
    def get_user_id(self):
        """
        Get the user id from the request
        username contains u:18963 => 18963 is the magento IDS
        """
        global user
        user = self.request.user
        user_id = user.username.split(":")
        if len(user_id) < 1:
            user_id = None
        else:
            user_id = user_id[1]
        return user_id

    def get(self, request, format=None):
        """
        Args:
            request :
                Get params:
                1. custemer id filter RevertPoinsTransection user based
        """
        user_id = self.get_user_id()
        mrewards_obj=MRewardsTransaction.objects.filter(customer__entity_id=user_id)
        if mrewards_obj:
            serializer = RewardPointSerializer(mrewards_obj, many=True)
            logger.info(" get all Rewards Transaction for the user {}".format(user_id))
            return Response(serializer.data)
        else:
            return Response({"status": False})
