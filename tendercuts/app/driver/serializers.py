from . import models as models

from rest_framework import serializers
from app.core.serializers import DriverSerializer, SalesOrderSerializer

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DriverLocation
        fields = ('driver', 'location', "updated")

