from rest_framework import serializers
from .. import models as models
from .driver_serializer import DriverSerializer


class GMapsStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GmapLangandlatisLongandlatis
        fields = ('latitude', 'longitude')


class GMapsStoreLinkSerializer(serializers.ModelSerializer):
    longandlatis = GMapsStoreSerializer()
    class Meta:
        model = models.GmapLangandlatisLongandlatisStore
        fields = ("longandlatis", )


class StoreSerializer(serializers.ModelSerializer):
    # reverse link
    location = GMapsStoreLinkSerializer()
    class Meta:
        model = models.CoreStore
        fields = ('name', "code", "store_id", "location", "website_id")
