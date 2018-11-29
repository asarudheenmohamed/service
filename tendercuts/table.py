from django.core.management.commands.inspectdb import Command
from django.conf import settings
from config.settings.local import DATABASES  #  replace `your_project_dir`

import django

if not settings.configured:
    settings.configure()

settings.DATABASES = DATABASES

django.setup()

tables = ['sales_flat_orders_address']
tables = ['salesrule']
tables = [ "catalog_product_entity_text",
          "catalog_product_entity_varchar"]

Command().execute(
    table=tables,#lambda table_name: table_name in tables,
    database='magento',
    no_color=True)
