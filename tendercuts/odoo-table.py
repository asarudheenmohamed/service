from django.core.management.commands.inspectdb import Command
from django.conf import settings
from config.settings.local import DATABASES  # replace `your_project_dir`

import django

if not settings.configured:
    settings.configure()

settings.DATABASES = DATABASES

django.setup()

tables = ["stock_warehouse", "stock_warehouse_tc_map_view_geohash_rel", "tc_map_view_geohash"]

Command().execute(
    table=tables,  # lambda table_name: table_name in tables,
    database='erp',
    no_color=True)
