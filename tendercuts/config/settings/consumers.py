import logging

from datetime import datetime, timedelta
from celery import bootsteps
from kombu import Consumer
from config.settings import celeryconfig
from django.conf import settings


logger = logging.getLogger(__name__)


class MageOrderChangeConsumer(bootsteps.ConsumerStep):
    """Customer consumer to route message"""

    def get_consumers(self, channel):
        """Add a customer consumer while celery starts to listen to order change Q.

        :param
            channel: MQ channel.
        """
        logger.info('Registering custom consumer')
        return [Consumer(channel,
                         queues=[celeryconfig.CUSTOM_QUEUES["ORDER_CHANGE"]],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def _send_retail_sms(self, message):
        """Callback that gets triggered when the order in payload is complete."""

        # One more way of calling.
        from app.driver import tasks

        scheduled_time = datetime.now() + timedelta(hours=4)
        scheduled_time = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")

        if str(message['medium']) == str(settings.ORDER_MEDIUM['POS']):
            tasks.send_sms.delay(
                message['increment_id'],
                'retail_complete',
                scheduled_time=scheduled_time)

    def _send_sms(self, message):
        """Callback that gets triggered when the order status changed.
            send sms to customer
        """
        from app.driver import tasks
        tasks.send_sms.delay(
            message['increment_id'],
            message['status'])

    def _on_update_order_elapsed_time(self, message):
        """Callback that gets triggered when the order in payload is complete,processing,out delivery."""

        # One more way of calling.
        from app.sale_order import tasks

        eta_time = datetime.utcnow() + timedelta(seconds=10)
        # eta set the task excution time
        tasks.update_order_elapsed_time.apply_async(
            (message['increment_id'], message['status']), eta=eta_time)

    def handle_message(self, body, message):
        """RMQ callback for handling the message/payload."""
        # {u'status': u'complete', u'increment_id': u'700018288'}

        retail_order_callbacks = {
            'complete': [self._send_retail_sms],

        }
        online_order_callbacks = {
            'pending': [self._on_update_order_elapsed_time, self._send_sms],
            'scheduled_order': [self._on_update_order_elapsed_time],
            'processing': [self._on_update_order_elapsed_time],
            'out_delivery': [self._on_update_order_elapsed_time],
            'complete': [self._on_update_order_elapsed_time],
            'canceled':[self._on_update_order_elapsed_time,self._send_sms],
            'closed':[self._on_update_order_elapsed_time]
        }

        # validations
        if 'status' not in body:
            message.ack()
            return

        status = body['status']

        if str(body['medium']) == str(settings.ORDER_MEDIUM['POS']):
            callbacks = retail_order_callbacks
        else:
            callbacks = online_order_callbacks

        # check for status callbacks
        if status in callbacks:
            for execute in callbacks[status]:
                execute(body)

        logger.info('Received message: {0!r}'.format(body))

        # ack for RMQ.
        message.ack()


from config.celery import app

app.steps['consumer'].add(MageOrderChangeConsumer)
