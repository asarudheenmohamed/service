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
# tables = ["sales_flat_order", "sales_flat_order_address", "sales_flat_order_item"]
tables = ["eav_attribute"]
Command().execute(
    table=tables,#lambda table_name: table_name in tables,
    database='magento',
    no_color=True)
