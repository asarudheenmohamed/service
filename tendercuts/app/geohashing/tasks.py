"""Sending unmapped customer geohash to related celery tasks."""

import logging

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import Mail
from config.celery import app


logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def geohash_mail(message):
    """Celery task to send mail for unmapped customer geohash."""
    logger.info("Sending geohash mail")
    Mail().send(
                "reports@tendercuts.in",
                ["hariharan@tendercuts.in", "varun@tendercuts.in"],
                "[CRITICAL] Unmapped Geohash of customer",
                message)