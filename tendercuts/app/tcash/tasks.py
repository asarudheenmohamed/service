"""Sending order's status sms to the customer related celery tasks."""

import logging

from config.celery import app

from app.core.lib.celery import TenderCutsTask

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def credit_referral_points(order_id):
    """Celery task to credit the customer with rewards poionts"""
    from app.tcash.lib.reward_points_controller import RewardsPointController

    RewardsPointController().add_referral_bonus(order_id)
