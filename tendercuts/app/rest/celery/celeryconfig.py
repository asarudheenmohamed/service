from datetime import timedelta

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Kolkata'


CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'rest.celery.tasks.cache_addresses',
        'schedule': timedelta(seconds=30),
    },
}
