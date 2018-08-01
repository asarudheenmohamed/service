"""
Custom celery task & related utils
"""

from __future__ import absolute_import

import os

import celery
from django.conf import settings

from .communication import Mail
from .exceptions import send_exception


class TenderCutsTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = '{0!r} failed: {1!r} errorinfo: {2!r}'.format(
            task_id, exc, einfo)
        send_exception("[CRITICAL] {}-Task failure".format(self.name), msg)
