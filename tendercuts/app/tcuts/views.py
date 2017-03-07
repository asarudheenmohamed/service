from . import serializers as serializers
from . import models as models

from rest_framework.views import APIView
from rest_framework import viewsets, generics
import json
import datetime
from rest_framework.response import Response

from rest_framework import status


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    queryset = models.CoreStore.objects.all()
    serializer_class = serializers.StoreSerializer
