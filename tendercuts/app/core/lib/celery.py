"""
Custom celery task & related utils
"""

from __future__ import absolute_import

from .communication import Mail
import celery

class TenderCutsTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = '{0!r} failed: {1!r}'.format(task_id, exc)
        Mail().send(
            "reports@tendercuts.in",
            ["tech@tendercuts.in"],
            "[CRITICAL] Task failure",
            msg)
