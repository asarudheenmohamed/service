import pytest
from django.conf import settings

from app.core.models import SalesruleCoupon
from app.tcash.lib.referral_code_controller import ReferralCodeController
import mock


@pytest.mark.django_db
def test_code_controller(monkeypatch):
    """Asserts:

    1\ check if the sales code is generated
    """
    controller = ReferralCodeController(27274)
    assert controller is not None

    def mock_load_basic_info(*args):
        return (27272, "test@test.com", "9908765678", 'Test User', 134)

    monkeypatch.setattr(
        ReferralCodeController, 'get_user_data', mock_load_basic_info)

    rule = controller.get_code()
    assert rule.code[:4] == "TEST"
    assert rule.user_id == 27272


@pytest.mark.django_db
def test_create_code():
    """
    When trying to create code, if the code already exists for another user
    then create a new once

    :return:
    """
    # Scene: TESTABC is already given to 2724 customer
    SalesruleCoupon.objects.filter(code="TESTBAC").delete()
    exist_code = "TESTABC"
    rule_id = settings.REFERRAL_RULE_ID
    rule, _ = SalesruleCoupon.objects.get_or_create(
        rule_id=rule_id,
        code=exist_code,
        usage_per_customer=1,
        times_used=0,
        type=1,
        user_id=27274
    )

    controller = ReferralCodeController(27275)

    # mock the generate code call, first time when called, it gives the existing
    # code
    controller._generate_code = mock.Mock()
    controller._generate_code.side_effect = ["TESTABC", "TESTABC", "TESTBAC"]

    code = controller._create_code(27275, "test")
    assert code.code == "TESTBAC"
    assert code.user_id == 27275

