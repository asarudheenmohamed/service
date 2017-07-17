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

# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Name and email addresses of recipients
ADMINS = (
    ('Varun Prasad', 'varun@tendercuts.in'),
    ('Asarudheen', 'asarudheen@tendercuts.in'),
    ('Tech Ops', 'tech-ops@tendercuts.in')
)

# Email address used as sender (From field).
SERVER_EMAIL = 'reports@tendercuts.in'

# Mailserver configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'reports@tendercuts.in'
EMAIL_HOST_PASSWORD = 'D%6Byz6+no;Dhgv2'