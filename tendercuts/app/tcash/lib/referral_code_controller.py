"""Enpoint for the generate a new coupon code."""

import random
import string

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

    def _generate_code(self, name):
        """Generates the code by taking first 4 letters of name
        and 3 random digits"""

        if len(name) > 4:
            name = name[:4]

        code = "".join([random.choice(
            string.ascii_uppercase + string.digits) for _ in range(3)])

        return "{}{}".format(name.upper(), code)

    def _create_code(self, user_id, name):
        """Gets or generates the unique ref code

        :param user_id: entityid of the user
        :param name: name

        :return: SalesruleCoupon
        """
        rule = None
        while not rule:
            # get the unique code
            code = self._generate_code(name)

            try:
                rule = SalesruleCoupon.objects.get(
                    rule_id=self.rule_id,
                    code=code,
                )  # type: (SalesruleCoupon, bool)
            except SalesruleCoupon.DoesNotExist:
                rule = SalesruleCoupon.objects.create(
                    rule_id=self.rule_id,
                    code=code,
                    usage_per_customer=1,
                    times_used=0,
                    type=1,
                    user_id=user_id
                )

            if rule.user_id != user_id:
                rule = None

        return rule

    def get_code(self):
        """Private method that generates and extracts the unique code for
        the customer

        :return:
        """
        # user_id, email, ph, name, reward pts
        data = self.get_user_data()
        user_id = data[0]
        name = data[3]

        try:
            rule = SalesruleCoupon.objects.get(
                rule_id=self.rule_id,
                user_id=user_id
            )  # type: (SalesruleCoupon, bool)
        except SalesruleCoupon.DoesNotExist:
            rule = self._create_code(user_id, name)

        return rule

    def get_message(self):
        """Generate the message to share with the user"""
        rule = self.get_code()

        return self.MESSAGE_TEMPLATE.format(rule.code)
