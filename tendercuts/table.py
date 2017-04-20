from django.core.management.commands.inspectdb import Command
from django.conf import settings
from config.settings.local import DATABASES  #  replace `your_project_dir`

import django

settings.configure()
settings.DATABASES = DATABASES

django.setup()

tables = ["catalog_product_entity", "catalog_product_entity_datetime", "catalog_product_entity_decimal",
          "catalog_product_entity_int", "catalog_product_entity_text", "catalog_product_entity_text",
          "catalog_product_entity_varchar"]
tables = ["catalog_category_flat_store_1", "catalog_category_flat_store_4", "catalog_category_flat_store_5",
"catalog_category_flat_store_7", "catalog_category_flat_store_8", "catalog_category_flat_store_9",
"catalog_category_entity"]
# tables = ["sales_flat_order", "sales_flat_order_address", "sales_flat_order_item"]
# tables = ["catalog_category_product", "catalog_category_entity"]
# tables = ["catalog_category_product"]
tables = ["customer_entity", "customer_entity_datetime",
"customer_entity_decimal", "customer_entity_int",
"customer_entity_text", "customer_entity_varchar"]
tables = ["rewardpoints_customer"]
tables = ["aitoc_cataloginventory_stock_item"]
tables = ["otp_list"]

tables = ["customer_address_entity", "customer_address_entity_datetime",
"customer_address_entity_decimal", "customer_address_entity_int",
"customer_address_entity_text", "customer_address_entity_varchar"]
tables = ["m_credit_balance"]
tables = ["sales_flat_quote"]

Command().execute(
    table=tables,#lambda table_name: table_name in tables,
    database='magento',
    no_color=True)
