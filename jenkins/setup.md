# Set up db instance
```bash
aws s3 ls s3://tendercuts-databackup/
aws s3 cp s3://tendercuts-databackup/tendercutsmysqldata-01-Mar-2018-15-35.tar.gz /tmp
```

# import the db into container
```bash 
cat backup/v2.sql| docker exec  -i mage-db /usr/bin/mysql -u root --password=root dbmaster
```

# Import views
```sql

CREATE FUNCTION `RUN_ALLOCATION_RULE`(store_type INT, online_allocation FLOAT, threshold FLOAT, qty FLOAT) RETURNS decimal(8,2)
    DETERMINISTIC
RETURN FORMAT_NUM(
      CASE
        WHEN store_type = 1 THEN (qty * online_allocation) - threshold
        WHEN store_type = 2 THEN qty
      END);

DROP FUNCTION IF EXISTS FORMAT_NUM;
CREATE FUNCTION FORMAT_NUM(qty FLOAT) RETURNS decimal(8,2)
    DETERMINISTIC
RETURN ROUND(
    GREATEST(IFNULL(qty, 0), 0),
    2);

-- Set up a helper function to convert KG to UNITS
DROP FUNCTION IF EXISTS CONVERT_TO_UNITS;
CREATE FUNCTION CONVERT_TO_UNITS(qty FLOAT, gpu INT)
  RETURNS INT DETERMINISTIC
  -- 0 incase no inventory is available.
  RETURN IFNULL(qty * IFNULL(1000/gpu, 1),0);


-- Function to compute inv for omni and dark store
DROP FUNCTION IF EXISTS INVENTORY;
CREATE FUNCTION INVENTORY(store_type INT, online_allocation FLOAT, threshold FLOAT, gpu INT, qty FLOAT)
  RETURNS FLOAT DETERMINISTIC
  RETURN CONVERT_TO_UNITS(
      CASE
        WHEN store_type = 1 THEN (qty * online_allocation) - threshold
        WHEN store_type = 2 THEN qty
      END, gpu);


-- Function to compute sch inv for omni and dark store
DROP FUNCTION IF EXISTS SCH_INVENTORY;
CREATE DEFINER=`root`@`localhost` FUNCTION `SCH_INVENTORY`(store_type INT, qty FLOAT, expiring FLOAT, forecast FLOAT) RETURNS decimal(8,2)
    DETERMINISTIC
RETURN FORMAT_NUM(
      CASE
        WHEN store_type = 1 THEN qty - expiring 
        WHEN store_type = 2 THEN forecast
      END);

DROP VIEW `graminventory_latest`;
CREATE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `graminventory_latest`
AS SELECT
    child.id,
    child.product_id,
    CONVERT_TO_UNITS(child.total_qty, child.gpu) as qty,
    CONVERT_TO_UNITS(child.total_scheduledqty, child.gpu) as scheduledqty,
    child.store_id,
    child.total_qty,
    child.total_expiring,
    child.total_forecast,
    child.gpu
FROM graminventory_latest_raw as child
LEFT JOIN graminventory_latest_raw as parent on child.parent = parent.product_id and child.store_id = parent.store_id;

DROP VIEW `graminventory_latest_raw`;
CREATE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `graminventory_latest_raw`
AS SELECT
   concat(`catalog`.`entity_id`,'-',`store`.`store_id`) AS `id`,
   `catalog`.`entity_id` AS `product_id`,
   `RUN_ALLOCATION_RULE`(`store`.`typeofstore`,
   `store`.`online_allocation`,
   `store`.`product_threeshold`,
   `inventory`.`qty`) AS `allocated_qty`,
   `RUN_ALLOCATION_RULE`(`store`.`typeofstore`,
   `store`.`online_allocation`,
   `store`.`product_threeshold`,
   `SCH_INVENTORY`(`store`.`typeofstore`,
   `inventory`.`qty`,
   `inventory`.`expiringtoday`,
   `inventory`.`forecastqty`)) AS `allocated_scheduledqty`,
   `FORMAT_NUM`(`inventory`.`qty`) AS `total_qty`,
   `SCH_INVENTORY`(`store`.`typeofstore`,
   `inventory`.`qty`,
   `inventory`.`expiringtoday`,
   `inventory`.`forecastqty`) AS `total_scheduledqty`,
   `parententity`.`entity_id` AS `parent`,
   `store`.`store_id` AS `store_id`,
   `FORMAT_NUM`(`inventory`.`expiringtoday`) AS `total_expiring`,
   `FORMAT_NUM`(`inventory`.`forecastqty`) AS `total_forecast`,
   `gpu`.`value` AS `gpu`
FROM (((((`catalog_product_entity` `catalog` join `storeattributes` `store`) left join `graminventory` `inventory` on(((`inventory`.`product_id` = `catalog`.`entity_id`) and (`inventory`.`store_id` = `store`.`store_id`) and (`inventory`.`date` = curdate())))) left join `catalog_product_entity_varchar` `gpu` on(((`gpu`.`attribute_id` = 229) and (`inventory`.`product_id` = `gpu`.`entity_id`)))) left join `catalog_product_entity_varchar` `parent` on(((`parent`.`attribute_id` = 230) and (`catalog`.`entity_id` = `parent`.`entity_id`)))) left join `catalog_product_entity` `parententity` on((`parententity`.`sku` = `parent`.`value`)));



```


# Set uo tendercuyts
```sql
	DELETE FROM core_config_data WHERE path='web/cookie/cookie_domain';
DELETE FROM core_config_data WHERE path='web/cookie/cookie_path';
UPDATE core_config_data
	SET VALUE = REPLACE(value, 'https://tendercuts.in', 'http://localhost')
    WHERE value like '%tendercuts.in%';
-- Optional
UPDATE core_config_data
	SET VALUE = REPLACE(value, 'http://d19owii3igrwxq.cloudfront.net', '{{unsecure_base_url}}')
    WHERE value like 'http://d19owii3igrwxq.cloudfront.net%';
UPDATE core_config_data
	SET VALUE = REPLACE(value, 'https://d19owii3igrwxq.cloudfront.net', '{{secure_base_url}}')
    WHERE value like 'https://d19owii3igrwxq.cloudfront.net%'
```