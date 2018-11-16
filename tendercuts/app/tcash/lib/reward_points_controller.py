"""Enpoint for the add New user reward amount."""

import logging
import datetime

from app.core.models.customer.entity import MRewardsTransaction
from app.core.models import SalesFlatOrder, SalesruleCoupon, CustomerEntityVarchar


class RewardsPointController:
    """EndPoint add transaction amount for the user."""

    def __init__(self, log=None):
        """Initialize amound value and expired date email sent value."""
        self.log = logging.getLogger('reward_pint')
        self.amount = 100
        self.is_expired = 0
        self.email_sent = 1

    def add_transaction(self, new_user_obj, referrer_obj):
        """DEPRECATED: Add Transaction amount for new refered user.

        params:
            new_user_obj(obj): request user object
            referrer_obj(obj): referer user objects

        Returns:
            Reward Transaction amount added request user object

        """
        reward_point_obj = MRewardsTransaction(
            customer=new_user_obj.customer, amount=self.amount,
            is_expired=self.is_expired,
            created_at=datetime.datetime.now(),
            is_expiration_email_sent=self.email_sent,
            comment='Gift from your friend {}'.format(
                referrer_obj._flat['firstname']))
        self.log.info("Add reward point amount for the new user  {}".format(
            new_user_obj.customer.entity_id))
        reward_point_obj.save()

        return reward_point_obj

    def _get_order(self, order_id):
        """Private method to ease testing"""
        return SalesFlatOrder.objects.get(increment_id=order_id)

    def _get_rule(self, coupon_code):
        """Private method to ease testing to get rul"""
        return SalesruleCoupon.objects.get(code=coupon_code)

    def _get_customer_id(self, ph_number):
        """Private method to ease testing to get rul"""
        return CustomerEntityVarchar.objects.get(
            attribute_id=149, value=ph_number)

    def add_referral_bonus(self, order_id):
        """Add Transaction amount for the order if it is a
        referred order

        params:
            order_id(obj): Increment id of the order

        Returns: None
        """

        order = self._get_order()

        # first check if the coupon code applied is a phone number of registered user
        if not order.coupon_code or len(order.coupon_code) != 10:
            return

        try:
            rule = self._get_rule(order.coupon_code)
        except SalesruleCoupon.DoesNotExist:
            return

        try:
            origin_customer = self._get_customer_id(rule.code)
        except CustomerEntityVarchar.DoesNotExist:
            self.log.debug("Unable to find user for coupon {}".format(
                order.coupon_code))
            return

        reward_point_obj = MRewardsTransaction(
            customer_id=origin_customer.entity_id,
            amount=self.amount,
            is_expired=self.is_expired,
            created_at=datetime.datetime.now(),
            is_expiration_email_sent=self.email_sent,
            comment='Referral bonus for referring your friend {}'.format(
                order.customer_firstname))
        self.log.info("Added reward point amount for existing users {}".format(
            order.entity_id))
        reward_point_obj.save()

        return reward_point_obj
