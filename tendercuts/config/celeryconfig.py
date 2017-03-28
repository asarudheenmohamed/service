from __future__ import absolute_import

from datetime import timedelta
from celery.schedules import crontab

# moving it here as the root is of no use.
CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Kolkata'


CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'app.payment_recon.tasks.cancel_payu_orders',
        'schedule': crontab(minute='*/5')
    },
}
