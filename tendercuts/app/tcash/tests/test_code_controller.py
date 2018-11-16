import mock
import pytest
from django.conf import settings

from app.core.models import SalesruleCoupon
from app.tcash.lib.referral_code_controller import ReferralCodeController
from app.tcash.lib.reward_points_controller import RewardsPointController


@pytest.mark.django_db
def test_code_controller(monkeypatch):
    """Asserts:

    1\ check if the sales code is generated
    """
    controller = ReferralCodeController(27274)
    assert controller is not None

    phone = 9908765678
    rule_id = settings.REFERRAL_RULE_ID
    rule = SalesruleCoupon.objects.filter(
        rule_id=rule_id,
        code=phone,
    ).delete()

    def mock_load_basic_info(*args):
        return (27272, "test@test.com", phone, 'Test User', 134)

    monkeypatch.setattr(
        ReferralCodeController, 'get_user_data', mock_load_basic_info)

    rule = controller.get_code()
    assert rule.code == phone


@pytest.mark.django_db
def test_referral_bonus_failure_with_non_ph_coupon(monkeypatch):
    """Asserts if coupon code no action is taken for failure"""

    def mock_order(*args):
        order = mock.Mock()
        order.coupon_code = "blah"
        return order

    monkeypatch.setattr(
        RewardsPointController, '_get_order', mock_order)

    assert RewardsPointController().add_referral_bonus(123) is None


@pytest.mark.django_db
def test_referral_bonus_failure_with_nocoupon(monkeypatch):
    """Asserts if coupon code no action is taken for failure"""

    def mock_order(*args):
        order = mock.Mock()
        order.coupon_code = None
        return order

    monkeypatch.setattr(
        RewardsPointController, '_get_order', mock_order)

    assert RewardsPointController().add_referral_bonus(123) is None


@pytest.mark.django_db
def test_referral_bonus_success(monkeypatch):
    """Asserts if coupon code no action is taken for failure"""

    def mock_order(*args):
        order = mock.Mock()
        order.coupon_code = "9908765678"
        return order

    def mock_user(*args):
        order = mock.Mock()
        order.entity_id = 1
        return order

    monkeypatch.setattr(
        RewardsPointController, '_get_order', mock_order)
    monkeypatch.setattr(
        RewardsPointController, '_get_customer_id', mock_user)

    obj = RewardsPointController().add_referral_bonus(123)
    assert obj is not None
    assert obj.amount == 100
