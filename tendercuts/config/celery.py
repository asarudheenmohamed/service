# import sys
# import os
# sys.path.remove(os.path.dirname(__file__)) 
# YOU NEED THIS OTHERWISE YOU"LL THE ISSUE OF
# NO MOFULE NAMED CELLARY
from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab
from kombu import  Queue
from django.conf import  settings

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
# django.setup()

app = Celery('tendercuts')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object(celeryconfig)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'every-minute': {
        'task': 'app.payment.tasks.check_payment_status',
        'schedule': crontab(minute='*/3')
    }
}

queues = [Queue('default', routing_key='task.#')]
queues.extend(settings.CELERY_QUEUES.values())

app.conf.task_queues = tuple(queues)

if __name__ == '__main__':
    app.start()
