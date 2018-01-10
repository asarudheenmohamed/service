"""
Just pay payment mode API calls
"""

import logging

from rest_framework import viewsets, mixins, status, renderers
from rest_framework.response import Response
from rest_framework.decorators import list_route

from app.core.lib.utils import get_user_id
from app.payment.lib.gateway import juspay
from .. import serializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class JuspayPaymentMethodViewSet(mixins.CreateModelMixin,
                                 viewsets.GenericViewSet):
    """
    A viewset that provides default `list()` actions.
    EndPoint:
        API: payment/payment_mode/
        API: payment/payment_mode/delete
    """
    serializer_class = serializer.PaymentModeSerializer

    def perform_create(self, serializer):
        """
        Overriding the perform create of the create MIXIN, to not only create
        the django model, but also create an entry in JP locker>
        """
        user_id = get_user_id(self.request)

        # returns the Transient model
        payment_mode = serializer.save()
        juspay.JuspayPaymentMode().add_payment_mode(user_id, payment_mode)

    @list_route(methods=['post'], renderer_classes=[renderers.JSONRenderer])
    def delete(self, request, *args, **kwargs):
        """"Override.
        Can't use the destroy mixin, because this is a transient model"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_mode = serializer.save()
        user_id = get_user_id(self.request)
        juspay.JuspayPaymentMode().remove_payment_mode(user_id, payment_mode)

        return Response({"status": True})
