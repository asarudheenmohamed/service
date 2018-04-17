import logging

from celery import bootsteps
from kombu import Consumer
from config.settings import celeryconfig

logger = logging.getLogger()


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

    def on_complete(self, message):
        """Callback that gets triggered when the order in payload is complete."""

        # One more way of calling.
        from app.driver import tasks

        tasks.send_sms.delay(message['increment_id'])

    def handle_message(self, body, message):
        """RMQ callback for handling the message/payload."""
        # {u'status': u'complete', u'increment_id': u'700018288'}

        callbacks = {
            'complete': self.on_complete,

        }

        # validations
        if 'status' not in body:
            message.ack()
            return

        # check for status callbacks
        body = eval(body)
        status = body['status']

        if status in callbacks:
            callbacks[status](body)

        logger.info('Received message: {0!r}'.format(body))

        # ack for RMQ.
        message.ack()


from config.celery import app

app.steps['consumer'].add(MageOrderChangeConsumer)
