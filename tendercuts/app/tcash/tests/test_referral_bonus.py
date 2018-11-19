import mock
import pytest

from app.tcash.lib.reward_points_controller import RewardsPointController


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
