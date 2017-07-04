"""Endpoint for  user reward points transaction."""
import logging
# Django Module
from .. import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from django.http import HttpResponse, JsonResponse
# Custom Module
from app.core.models.customer.entity import MRewardsTransaction
from app.login.serializer.serializers import RewardPointSerializer

logger = logging.getLogger(__name__)
# Get an instance of a logger


class RewardPointsTransaction(viewsets.ReadOnlyModelViewSet):
    """Endpoind for Fetch user based Reward point transaction data.

    Returns:
        user/fetch : Gets the user Reward point transaction data

    """
    serializer_class = RewardPointSerializer

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

    def get_queryset(self):
        """Endpoint fetch user reward point transection."""
        user_id = self.get_user_id()
        queryset = MRewardsTransaction.objects.filter(
            customer__entity_id=user_id)
        logger.info(" Get Reward Points Transaction for the user {}".format(
            user_id))
        return queryset
