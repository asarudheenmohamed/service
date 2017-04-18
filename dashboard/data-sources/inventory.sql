-- 71: Product Name
-- 96: Status [Only Active onlye]
-- 102: Visibility
-- store_id not needed
select 
    inv.product_id,
    vars.value as name,
    product.sku,
    store.code as Store,
    inv.qty

from aitoc_cataloginventory_stock_item as inv
join core_store store on store.website_id = inv.website_id
join catalog_product_entity as product on product.entity_id = inv.product_id
join catalog_product_entity_varchar as vars
	on vars.entity_id = inv.product_id and vars.attribute_id = 71 and vars.store_id = store.store_id
join catalog_product_entity_int as status_int 
	on product.entity_id = status_int.entity_id and status_int.attribute_id = 96
	and status_int.value = 1 and status_int.store_id = store.store_id
join catalog_product_entity_int as visibility_int
	on product.entity_id = visibility_int.entity_id and visibility_int.attribute_id = 102
	and visibility_int.value = 4 and visibility_int.store_id = store.store_id
where inv.website_id !=12 and store.store_id != 9
order by qty;