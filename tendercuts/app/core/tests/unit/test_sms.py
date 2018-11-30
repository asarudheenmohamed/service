"""End Point for the test SMS controller."""
import pytest
from app.core.lib.communication import SMS


@pytest.mark.django_db
class TestSMSController:
    """Test OTP controller."""

    def test_send_sms(self):
        """Test send_sms functionality.

        Asserts:
            Checks response status equal to 200.
            Checks the response message.

        """
        response = SMS().send_sms(
            9080600507,
            'Your order #1223324, is now out for delivery. Have a great meal Wish to serve you again!')

        assert response.status_code == 200
        assert response.text == 'Sent.'
