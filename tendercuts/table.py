from django.core.management.commands.inspectdb import Command
from django.conf import settings
from config.settings import DATABASES  #  replace `your_project_dir`

import django

settings.configure()
settings.DATABASES = DATABASES

django.setup()

tables = ["sales_flat_order_payment"]
# tables = ["sales_flat_order", "sales_flat_order_address", "sales_flat_order_item"]
Command().execute(
    table=tables,#lambda table_name: table_name in tables,
    database='magento',
    no_color=True)
