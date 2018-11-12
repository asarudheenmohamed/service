from rest_framework import serializers
from .. import models as models
from . import attribute
from . import product

# thumb is a generated property with CDN
PRODUCT_FIELDS = ('thumb', 'image', 'is_active', 'name', "entity_id")

class CatalogCategoryFlatStore1Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore1
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore4Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore4
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore5Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore5
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore7Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore7
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore8Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore8
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore9Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore9
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore10Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore10
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore11Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore11
        fields = PRODUCT_FIELDS


class CatalogCategoryFlatStore12Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore12
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore14Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore14
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore15Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore15
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore16Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore16
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore18Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore18
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore21Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore21
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore24Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore24
        fields = PRODUCT_FIELDS

class CatalogCategoryFlatStore26Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.CatalogCategoryFlatStore26
        fields = PRODUCT_FIELDS
