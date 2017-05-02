"""
Test cases for sending SMS
"""

import pytest
from app.core.lib.communication import SMS, Mail

@pytest.fixture
def sms():
    """
    Fixture to generate an sms instance
    """
    return SMS()

@pytest.fixture
def mail():
    """
    Fixture to generate an mail instance
    """
    return Mail()

def _test_dummy_sms(sms):
    """
    A pathetic test case to test sms
    """
    sms.send("9908765678", "HI")

def test_dummy_mail(mail):
    """
    Verify:
     Mail send
    """
    mail.send(
        "reports@tendercuts.in",
        ["varun@tendercuts.in"],
        "Hi",
        "Mailer")



