from rest_framework import serializers
from .. import models as models
from . import attribute

PRODUCT_FIELDS = ('price', 'short_description', 'description', 'sku',
                  "thumb",
                  "weight_description", "gross_weight_description",
                  "visibility", "status", "uom", "name", "entity_id",
                  "spicy","gramsperunit","weight_from","weight_to"
                  )


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


class CatalogProductFlat10Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat10
        fields = PRODUCT_FIELDS


class CatalogProductFlat11Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat11
        fields = PRODUCT_FIELDS


class CatalogProductFlat12Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat12
        fields = PRODUCT_FIELDS

class CatalogProductFlat14Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat14
        fields = PRODUCT_FIELDS

class CatalogProductFlat15Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat15
        fields = PRODUCT_FIELDS

class CatalogProductFlat16Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat16
        fields = PRODUCT_FIELDS

class CatalogProductFlat18Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat18
        fields = PRODUCT_FIELDS

class CatalogProductFlat21Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogProductFlat21
        fields = PRODUCT_FIELDS
