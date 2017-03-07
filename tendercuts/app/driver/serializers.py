from rest_framework import serializers
from . import models as models

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DriverLocation
        fields = ('driver', 'location', "updated")

