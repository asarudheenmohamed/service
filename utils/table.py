from django.core.management.commands.inspectdb import Command
from django.conf import settings
from config.settings import DATABASES  #  replace `your_project_dir`

settings.configure()
settings.DATABASES = DATABASES

tables = ["driver_management"]
Command().execute(
    table_name_filter=lambda table_name: table_name in tables,
    database='default',
    no_color=True)
