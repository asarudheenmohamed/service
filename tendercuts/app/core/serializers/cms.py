"""Serializers for the Cms models."""
from rest_framework import serializers
from .. import models as models


class CmsSerializer(serializers.ModelSerializer):
    """Serializer for the CmsPage Model."""
    class Meta:
        model = models.CmsPage
        fields = "__all__"
