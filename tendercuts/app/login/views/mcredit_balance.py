"""Endpoint for user Credit Balance transaction."""
import logging

from django.http import HttpResponse, JsonResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# Custom Module
from app.core.models.customer.entity import MCreditBalance
from app.login.serializer.serializers import McreditBalanceSerializer
from app.core.lib.utils import get_user_id

# Django Module
from .. import serializers

logger = logging.getLogger(__name__)
# Get an instance of a logger


class CreditBalance(viewsets.ReadOnlyModelViewSet):
    """Fetch user based Credit Balance.

    user/fetch : Gets the user user Credit Balance data

    """
    serializer_class = McreditBalanceSerializer

    def get_queryset(self):
        """Get the MCreditBalance from the request."""
        user_id = get_user_id(self.request)
        queryset = MCreditBalance.objects.filter(
            customer__entity_id=user_id)
        logger.info(" Get Credit Balance for the user {}".format(
            user_id))
        return queryset
