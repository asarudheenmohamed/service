"""
Custom celery task & related utils
"""

from __future__ import absolute_import

import os

import celery
from django.conf import settings

from .communication import Mail


class TenderCutsTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = '{0!r} failed: {1!r}  error:{2!r}'.format(task_id, exc, einfo)
        if os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.prod':
            Mail().send(
                settings.CELERY_MAIL['sender_mail_id'],
                settings.CELERY_MAIL['received_mail_id'],
                "[CRITICAL] Task failure",
                msg)
        elif os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.staging':
            Mail().send(
                settings.CELERY_MAIL['sender_mail_id'],
                settings.CELERY_MAIL['received_mail_id'],
                "[CRITICAL] Task failure in Staging",
                msg)
