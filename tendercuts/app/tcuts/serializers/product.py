from rest_framework import serializers
from .. import models as models
from . import attribute


class CatalogProductEntityDatetimeSerializer(serializers.ModelSerializer):
    attribute = attribute.EavAttributeSerializer()
    class Meta:
        model = models.CatalogProductEntityDatetime
        fields = ('value', 'attribute')


class CatalogProductEntityDecimalSerializer(serializers.ModelSerializer):
    attribute = attribute.EavAttributeSerializer()
    class Meta:
        model = models.CatalogProductEntityDecimal
        fields = ('value', 'attribute')


class CatalogProductEntityIntSerializer(serializers.ModelSerializer):
    attribute = attribute.EavAttributeSerializer()
    class Meta:
        model = models.CatalogProductEntityInt
        fields = ('value', 'attribute')


class CatalogProductEntityTextSerializer(serializers.ModelSerializer):
    attribute = attribute.EavAttributeSerializer()
    class Meta:
        model = models.CatalogProductEntityText
        fields = ('value', 'attribute')


class CatalogProductEntityVarcharSerializer(serializers.ModelSerializer):
    attribute = attribute.EavAttributeSerializer()
    class Meta:
        model = models.CatalogProductEntityVarchar
        fields = ('value', 'attribute')


class CatalogProductEntitySerializer(serializers.ModelSerializer):
    # entity_id = CatalogProductEntityDecimalSerializer(many=True)
    dates = CatalogProductEntityDatetimeSerializer(many=True)
    ints = CatalogProductEntityIntSerializer(many=True)
    # entity_id = CatalogProductEntityVarcharSerializer(many=True)
    # text = CatalogProductEntityTextSerializer(many=True)

    class Meta:
        model = models.CatalogProductEntity
        fields = ( 'sku', "dates", "ints")
             # 'date', 'integer',
            # 'string', 'text')


