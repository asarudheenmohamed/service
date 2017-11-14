"""Endpoint for  user reward points transaction."""
import logging

from django.http import HttpResponse, JsonResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# Custom Module
from app.core.models.customer.entity import MRewardsTransaction
from app.login.serializer.serializers import RewardPointSerializer
from app.core.lib.utils import get_user_id
# Django Module
from .. import serializers

logger = logging.getLogger(__name__)
# Get an instance of a logger


class RewardPointsTransaction(viewsets.ReadOnlyModelViewSet):
    """Endpoind for Fetch user based Reward point transaction data.

    Returns:
        user/fetch : Gets the user Reward point transaction data

    """
    serializer_class = RewardPointSerializer

    def get_queryset(self):
        """Endpoint fetch user reward point transection."""
        user_id = get_user_id(self.request)
        queryset = MRewardsTransaction.objects.filter(
            customer__entity_id=user_id).order_by('-created_at')
        logger.info(" Get Reward Points Transaction for the user {}".format(
            user_id))
        return queryset
