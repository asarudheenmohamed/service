# import sys
# import os
# sys.path.remove(os.path.dirname(__file__)) 
# YOU NEED THIS OTHERWISE YOU"LL THE ISSUE OF
# NO MOFULE NAMED CELLARY
from __future__ import absolute_import

from celery import Celery
from . import celeryconfig

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

app = Celery('tendercuts',
             broker='redis://localhost',
             backend='redis://localhost')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object(celeryconfig)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
