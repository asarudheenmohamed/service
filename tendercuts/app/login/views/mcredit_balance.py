"""Endpoint for user Credit Balance transaction."""
import logging
# Django Module
from .. import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from django.http import HttpResponse, JsonResponse
# Custom Module
from app.core.models.customer.entity import MCreditBalance
from app.login.serializer.serializers import McreditBalanceSerializer

logger = logging.getLogger(__name__)
# Get an instance of a logger


class CreditBalance(viewsets.ReadOnlyModelViewSet):
    """Fetch user based Credit Balance.

    user/fetch : Gets the user user Credit Balance data

    """
    serializer_class = McreditBalanceSerializer

    def get_user_id(self):
        """Get the user id from the request.

        Returns:
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
        """Get the MCreditBalance from the request."""
        user_id = self.get_user_id()
        queryset = MCreditBalance.objects.filter(
            customer__entity_id=user_id)
        logger.info(" Get Credit Balance for the user {}".format(
            user_id))
        return queryset
