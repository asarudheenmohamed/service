"""Enpoint for the generate a new coupon code."""

from django.conf import settings

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesruleCoupon


class ReferralCodeController:
    """EndPoint add transaction amount for the user."""

    MESSAGE_TEMPLATE = """Get Farm Fresh Meat & Fish delivered at home by TenderCuts. Use code {} & get 100 off on your 1st order. Download our App https://tcuts.in/4Mi5ZloXPR"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.rule_id = settings.REFERRAL_RULE_ID

    def get_user_data(self):
        """Branching into a separate method for testing convenience"""
        user_basic_info = CustomerSearchController.load_basic_info(self.user_id)
        return user_basic_info

    def get_code(self):
        """Private method that generates and extracts the unique code for
        the customer

        :return:
        """
        # user_id, email, ph, name, reward pts
        phone = self.get_user_data()[2]

        try:
            rule = SalesruleCoupon.objects.get(
                rule_id=self.rule_id,
                code=phone,
            )  # type: (SalesruleCoupon, bool)
        except SalesruleCoupon.DoesNotExist:
            rule = SalesruleCoupon.objects.create(
                rule_id=self.rule_id,
                code=phone,
                usage_per_customer=1,
                times_used=0,
                type=1
            )

        return rule

    def get_message(self):
        """Generate the message to share with the user"""
        rule = self.get_code()

        return self.MESSAGE_TEMPLATE.format(rule.code)


