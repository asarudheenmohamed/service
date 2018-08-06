from __future__ import absolute_import
from kombu import Exchange, Queue


BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
# 20 hrs
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 20


CELERY_QUEUES = {
}


CELERY_EXCHANGES = {
    # Exchange that handles all order state change messages.
    "ORDER_STATUS_CHANGE": Exchange("tendercuts.exchange.order.onchange", type='topic', durable=True)
}


CUSTOM_QUEUES = {
    # Q that will be consumed by our custom consumer, messages won't have
    # task headers, like ID and Task names.
    "ORDER_CHANGE": Queue(
        name="tendercuts.queue.order.status",
        durable=True,
        routing_key="order.*",
        exchange=CELERY_EXCHANGES['ORDER_STATUS_CHANGE'])
}
