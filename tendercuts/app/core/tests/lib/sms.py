import pytest
from app.core.lib.communication import SMS, Mail

@pytest.fixture
def sms():
    return SMS()

@pytest.fixture
def mail():
    return Mail()

def _test_dummy_sms(sms):
    sms.send("9908765678", "HI")

def test_dummy_mail(mail):
    mail.send(
        "reports@tendercuts.in",
        ["varun@tendercuts.in"],
        "Hi",
        "Mailer")



