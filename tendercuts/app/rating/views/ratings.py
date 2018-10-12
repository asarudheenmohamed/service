"""Endpoint to the Customer product rating for the purchased order."""

import logging

from app.rating import tasks
from app.rating.models import Rating, RatingTag
from app.rating.serializer.serializers import (ProductratingSerializer,
                                               ProductRatingTagSerializer)
from rest_framework import mixins, renderers, status, viewsets
from rest_framework.response import Response
from app.rating.lib import RatingController
from app.core import models


# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProductratingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Endpoint to the Customer update the product rating.

    EndPoint:
        API: rating/rating_create/
    """
    serializer_class = ProductratingSerializer

    def create(self, request, *args, **kwargs):
        """Driver assignment  endpoint.

        Params:
            Rating request dict object like {"order_id":2343546, "rating": 2, "comments": "erfwrwer", "rating_tag": [4, 5]}

        returns:
            Response({status: bool, message: str})

        """
        data = request.data.copy()
        data.update({'customer': unicode(self.request.user.id)})

        serializer = self.get_serializer(data=data)
        status = False

        queryset = models.SalesFlatOrder.objects \
       .filter(customer_id=self.request.user.id, status='complete') \
       .order_by('-created_at') \
       .prefetch_related("items") \
       .prefetch_related("payment") \
       .prefetch_related("shipping_address")[:2]

        if serializer.is_valid():
            serializer.save()
            if data['rating'] <= 3:
                tasks.create_fresh_desk_ticket.delay(data['increment_id'])

            if data['rating'] <= 3:
                tasks.create_fresh_desk_ticket.delay(data['increment_id'])

            return Response(
                {'status': True, 'message': 'Rating update successfully'}, status=status.HTTP_201_CREATED)

        return Response({'status': False, 'message': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class ProductRatingTagViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple ViewSet for viewing Rating Tags.
    """
    queryset = RatingTag.objects.all()
    serializer_class = ProductRatingTagSerializer
