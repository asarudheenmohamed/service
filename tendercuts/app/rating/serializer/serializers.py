"""Serializer for Rating and RatingTag models."""

from rest_framework import serializers
from app.rating.models import RatingTag, Rating


class ProductratingSerializer(serializers.ModelSerializer):
    """Rating model serializer."""

    class Meta:
        model = Rating
        fields = '__all__'


class ProductRatingTagSerializer(serializers.ModelSerializer):
    """RatingTag model serializer."""

    class Meta:
        model = RatingTag
        fields = '__all__'
