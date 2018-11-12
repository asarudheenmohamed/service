"""Scrip to remap stores for customers"""
import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()


from app.core.models import CustomerAddressEntityVarchar
from app.core.models import CoreStore
from app.geohashing.models.geocodes import (StockWarehouseTcMapViewGeohashRel, TcMapViewGeohash, StockWarehouse)

import pandas as pd

def get_consolidated_df():
    """

    Steps:
        1. Load the geohashes and store_ids, and inject the store name
        2. From odoo load the current geohashes.

    return
        pd.DataFrame(entity_id, geohash, old_store, old_store_id, new_store)
    """

    # Step 1
    geohashes = CustomerAddressEntityVarchar.objects.filter(attribute_id=244).values_list('entity_id', 'value')
    df = pd.DataFrame(list(geohashes), columns=['entity_id', 'geohash'])

    stores = CustomerAddressEntityVarchar.objects.filter(attribute_id=231).values_list('entity_id', 'value')
    store_df = pd.DataFrame(list(stores), columns=['entity_id', 'old_store'])

    data_df = df.merge(store_df, how='left')
    data_df = data_df[-data_df.old_store.isnull()]
    data_df = data_df[-data_df.geohash.isnull()]
    stores = CoreStore.objects.all().values_list('code', 'store_id')
    store_map = dict(list(stores))

    data_df['old_store_id'] = data_df.old_store.map(store_map)
    data_df = data_df[-data_df.old_store_id.isnull()]
    data_df.old_store_id = data_df.old_store_id.astype(int)
    # data_df => [entity_id, geohash, old_store, old_store_id]


    # step 2: Gather all the geohashes and create a dict of geohash id -> hash_id
    all_geohashes = TcMapViewGeohash.objects.all().values_list('id', 'hash_id')
    all_geohashes = dict(list(all_geohashes))

    # create a dict of warehouse id -> mage_code
    odoo_wh = StockWarehouse.objects.all().values_list('id', 'mage_code')
    odoo_wh= dict(list(odoo_wh))

    rels = StockWarehouseTcMapViewGeohashRel.objects.all().values_list(
        'stock_warehouse_id', 'tc_map_view_geohash_id')
    rels = pd.DataFrame(list(rels), columns=['new_store', 'geohash'])
    rels.geohash = rels.geohash.map(all_geohashes)
    rels.new_store = rels.new_store.map(odoo_wh)

    merged_df = data_df.merge(rels, how='inner')
    merged_df = merged_df[merged_df.new_store != merged_df.old_store]

    return merged_df

print ("Getting mismatches")
merged_df = get_consolidated_df()
#merged_df = merged_df[(merged_df.old_store == 'kattupakkam') | (merged_df.new_store == 'kattupakkam')]
for key, group in merged_df.groupby('new_store'):
    #data = CustomerAddressEntityVarchar.objects.filter(entity_id__in=group.entity_id.tolist(), attribute_id=231)
    #data.update(value=key)
    print (key)
    print (group)
    print ("============================")
print (len(merged_df))

