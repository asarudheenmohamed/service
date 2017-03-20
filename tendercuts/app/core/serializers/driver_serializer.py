from rest_framework import serializers
from .. import models as models

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DriverManagement
        fields = ('entity_id', 'name', "phone")

