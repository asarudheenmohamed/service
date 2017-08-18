from __future__ import absolute_import
from kombu import  Exchange, Queue


CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Asia/Kolkata'

CELERY_EXCHANGES = {
    # Exchange that handles all order state update messages.
    "ORDER_STATUS_UPDATE":  Exchange("tendercuts.exchange.order.update", type='fanout', durable=True),
    # Exchange that handles all order state change messages.
    "ORDER_STATUS_CHANGE":  Exchange("tendercuts.exchange.order.onchange", type='topic', durable=True)
}


CELERY_QUEUES = {
    # dummy queue to logs all messages
    "LOG_STATUS_CHANGE": Queue(
            name="tendercuts.queue.order.log",
            durable=True,
            routing_key="order.*",
            exchange=CELERY_EXCHANGES['ORDER_STATUS_CHANGE'])
}

