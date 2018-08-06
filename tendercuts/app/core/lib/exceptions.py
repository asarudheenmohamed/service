from app.core.lib.communication import Mail
from django.conf import settings
import os

class OrderNotFound(Exception):
    pass


class AuthenticationException(Exception):
    """Authendication Exception."""

    pass


class CustomerNotFound(AuthenticationException):
    """Customer object not found Exception."""

    pass


class InvalidCredentials(AuthenticationException):
    """Invalid credentials Exception."""

    pass


def send_exception(subject, msg):
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.prod':
        Mail().send(
            settings.CELERY_MAIL['sender_mail_id'],
            settings.CELERY_MAIL['received_mail_id'],
            subject,
            msg)
    elif os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.staging':
        Mail().send(
            settings.CELERY_MAIL['sender_mail_id'],
            settings.CELERY_MAIL['received_mail_id'],
            "[STAGING]{}".format(subject),
            msg)
