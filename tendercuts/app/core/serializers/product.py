from rest_framework import serializers
from .. import models as models
from . import attribute

PRODUCT_FIELDS = ('price', 'short_description', 'description', 'sku',
            "small_image", "thumbnail", 
            "weight_description", "gross_weight_description",
            "visibility", "status", "uom", "name", "entity_id")


class CatalogProductFlat1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat1
        fields = PRODUCT_FIELDS


class CatalogProductFlat4Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat4
        fields = PRODUCT_FIELDS


class CatalogProductFlat5Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat5
        fields = PRODUCT_FIELDS


class CatalogProductFlat7Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat7
        fields = PRODUCT_FIELDS


class CatalogProductFlat8Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat8
        fields = PRODUCT_FIELDS


class CatalogProductFlat9Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat9
        fields = PRODUCT_FIELDS
