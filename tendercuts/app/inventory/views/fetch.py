"""
Api endpoint to fetch the inventory
"""

import datetime
import itertools
import json

from django.db.models import F
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import models as models


class InventoryViewSet(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide the inventory for Day D
    """

    def merge_lists(self, l1, l2, key):
        """
        Merges the two lists.

        params:
            l1 (list of dicts): Inventory data from which today's inv needs
                to be fetched eg [{product : 1, qty: 4}]
            l2 (CatalogProductFlat1) Product data containing scheduled inv.
                eg [{product: 1, scheduledqty: 10}]
            key (string): Attributed based in which the inventory should
                be merged

        returns:
            a list for merged data
            eg: [{product: 1, qty: 4, scheduledqty: 10}]

        """
        merged = {}
        # list of dicts containning keys: product and qty|scheduledQty
        # join them on product IDs
        for item in list(l1) + list(l2):
            if item[key] in merged:
                merged[item[key]].update(item)
            else:
                merged[item[key]] = item

        values = []
        for (_, val) in merged.items():
            # double check if both quantity and schedule qty are present
            val.setdefault("qty", 0)
            scheduled_qty = val.setdefault("scheduledqty", 0)
            # In case it is set as none in DB, then replace with 0
            if scheduled_qty is None:
                val['scheduledqty'] = 0

            values.append(val)

        return values

    def get(self, request):
        """
        CatalogProductFlat1 contains global attributes such as sch delivery
        Aitoc contains per store inventory

        Fetch today's inventory from aitoc table and scheduled from scheduled
        tables

        params:
            request:
                1. store_id int - specifies the store id
                2. website_id - aitoc has this stupid thing of website id
                3. product_id (optional, list) - filter only those ids

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
