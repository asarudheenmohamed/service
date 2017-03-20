import datetime
import json

from . import models
from . import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status



class SalesOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    queryset = models.SalesFlatOrder.objects.all()
    serializer_class = serializers.SalesOrderSerializer


