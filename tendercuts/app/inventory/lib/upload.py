"""Controller for inventory uploading"""

import logging

from rest_framework.views import APIView

from app.core.models import CoreStore, AitocCataloginventoryStockItem
from .. import models as models


logger = logging.getLogger(__name__)


class InventoryUploadController(object):
    """Controller to upload the inventory.

    Expects the data in this format:
    Index([ u'PID',            u'PRODUCT',    u'UNITS',
            u'SKU WT',         u'Unnamed: 4', u'adayar',
            u'thoraipakkam',   u'porur',      u'tambaram',
            u'arumbakkam',     u'tpos',       u'adayar.1',
            u'thoraipakkam.1', u'porur.1',    u'tambaram.1',
            u'arumbakkam.1',   u'tpos.1',     u'Total Qty'],
      dtype='object')

    Here 1 is the closing stock and non one are processed data.
    """

    def __init__(self, inventory):
        """Constructors."""
        self.inventory = inventory

    def cleanup(self):
        """Clean up the df and prepares them for upload.

        1. Fill in all zeros for missing values.
        2. Skip rows that have no product IDs
        3. Reindex with Product ID
        4. drop unwated cols

        Afte this the DF is formatted as

            adayar  thoraipakkam  ...  adayar.1  thoraipakkam.1 ...
        PID
        319 5       6 ...
        """
        self.inventory = self.inventory.fillna(0)

        # Ignore all row with now PID
        # and format it and set it as index
        self.inventory = self.inventory[self.inventory.PID != 0]
        self.inventory.PID = self.inventory.PID.astype(int)
        self.inventory = self.inventory.set_index("PID")

        # Drop useless columns
        ignore_cols = ["PRODUCT", "UNITS", "SKU WT", "Unnamed: 4"]
        self.inventory.drop(ignore_cols, axis=1, inplace=True)

    def process(self):
        """Process the data and update our database.

        At this point he DF shoulb be indexable by product id and store name
        1. Add procesing and closing
        2. update data.

        """
        self.cleanup()
        # Get all store in {webid => store}
        store_cache = {
            store.website_id: store for store in CoreStore.objects.all()}

        inventories = AitocCataloginventoryStockItem.objects.all() \
            .select_related('product')

        self.inventory = self.inventory.astype(int)
        for inventory in inventories:
            try:
                store = store_cache[inventory.website_id]
                # get processed value
                qty = self.inventory.ix[inventory.product.entity_id, store.name]
                # get closing value
                closing = self.inventory.ix[
                    inventory.product.entity_id, store.name + ".1"]

                # update and save obj
                inventory.qty = qty + closing
                inventory.save()
            except KeyError:
                logger.error("No inv found for {} for {}".format(
                    inventory.product.sku, store.name))
