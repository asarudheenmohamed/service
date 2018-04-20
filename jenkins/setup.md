# Set up db instance
```bash
aws s3 ls s3://tendercuts-databackup/
aws s3 cp s3://tendercuts-databackup/tendercutsmysqldata-01-Mar-2018-15-35.tar.gz /tmp
```

# import the db into container
```bash 
cat backup/v2.sql| docker exec  -i mage-db /usr/bin/mysql -u root --password=root dbmaster
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

# In case magento does not restore properly
- 1. Try to remove cache
- 2. run the following command
```bash
chown -R www-data:www-data *
```