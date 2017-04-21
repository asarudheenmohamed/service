from . import models as models

from rest_framework.views import APIView
from rest_framework import viewsets, generics
import json
import datetime
from rest_framework.response import Response
import itertools
from rest_framework import status
from django.db.models import F



class InventoryViewSet(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # queryset = models.CatalogProductFlat1.objects.all()
    # serializer_class = serializers.CatalogProductFlat1Serializer
    def merge_lists(self, l1, l2, key):
        merged = {}
        for item in list(l1) + list(l2):
            if item[key] in merged:
                merged[item[key]].update(item)
            else:
                merged[item[key]] = item

        return [val for (_, val) in merged.items()]

    def get(self, request):
        """
        CatalogProductFlat1 contains global attributes such as sch delivery
        Aitoc contains per store inventory
        """
        store_id = self.request.GET['store_id']
        website_id = self.request.GET['website_id']
        product_ids = self.request.GET.get("product_ids", [])

        if product_ids:
            product_ids = product_ids.split(",")
            future = models.CatalogProductFlat1.objects.filter(
                entity__entity_id__in=product_ids)
            today = models.AitocCataloginventoryStockItem.objects.filter(
                product__entity_id__in=product_ids)
        else:
            future = models.CatalogProductFlat1.objects.all()
            today = models.AitocCataloginventoryStockItem.objects.all()

        # rename entity_id to product andfetch only sch deliveyr
        future = future.annotate(product=F("entity_id")) \
            .values('product', 'scheduledqty')

        today = today.filter(website_id=website_id).values('product', 'qty')


        inventory = self.merge_lists(today, future, "product")

        return Response(inventory)



