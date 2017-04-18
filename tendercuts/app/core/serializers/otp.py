from rest_framework import serializers
from .. import models as models


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OtpList
        fields = ('mobile', 'otp')

