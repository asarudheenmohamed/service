from __future__ import absolute_import

from datetime import timedelta
from celery.schedules import crontab

# moving it here as the root is of no use, and setting it to socket
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# ONLY IN PROD
# CELERY_BROKER_URL = 'redis+socket:///var/run/redis/redis.sock'
# CELERY_RESULT_BACKEND = 'redis+socket:///var/run/redis/redis.sock'


CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Kolkata'
