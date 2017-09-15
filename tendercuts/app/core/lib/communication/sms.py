"""End point for the send sms to the customer mobile number."""
import requests
import sendotp
from django.conf import settings


class OldSMS():
    """
    SMS class that has the send interface.

    Note: This is deprecated in favor of MSG 91
    """

    def __init__(self):
        pass

    def send(self, phnumber, message):
        """Send the message.

        params:
            phnumber (int): Ph number to send
            message (str): message

        raises:
            Error in case of bad/invalid request

        """
        data = {
            "method": "sms",
            "api_key": settings.SMS_GATEWAY["KEY"],
            "sender": settings.SMS_GATEWAY['SENDER_ID'],
            "to": phnumber,
            "message": message
        }

        resp = requests.post(
            settings.SMS_GATEWAY["ENDPOINT"],
            data=data)

        # Raise error
        resp.raise_for_status()


class SMS():
    """New sms class based on msg91."""

    def __init__(self):
        """Initialize the msg9 auth key."""
        self.otp = sendotp.sendotp(
            settings.SMS_GATEWAY["KEY"],
            "")

    def send(self, phnumber, message):
        """Send the message.

        params:
            phnumber (int): Ph number to send
            message (str): message

        raises:
            Error in case of bad/invalid request

        """
        data = {
            "authkey": settings.SMS_GATEWAY["KEY"],
            "mobiles": phnumber,
            "message": message,
            "sender": settings.SMS_GATEWAY["SENDER_ID"],
            "route": 4,
            "country": 91
        }

        requests.get(
            settings.SMS_GATEWAY["ENDPOINT"],
            verify=False,
            params=data)

    def send_otp(self, phnumber, message, otp):
        """Send OTP.

        Sends the OTP, new interface because of the stupid msg91's interface

        params:
            phnumber (int): Ph number to send
            OTP (str): OTP message
            message (str): message

        raises:
            Error in case of bad/invalid request

        """
        phnumber = "%s%s" % ("91", str(phnumber))
        self.otp.msg = message
        otp = self.otp.send(
            phnumber,
            settings.SMS_GATEWAY["SENDER_ID"],
            otp)

    def retry_otp(self, phnumber, retry_mode):
        """Resend OTP.

        Resends the OTP, new interface because of the stupid msg91's interface

        params:
            phnumber (int): Customer mobile number
            retry_mode (str): retry OTP type such as text or voice

        raises:
            Error in case of bad/invalid request

        """
        phnumber = "%s%s" % ("91", str(phnumber))
        data = {
            "authkey": settings.SMS_GATEWAY["KEY"],
            "mobile": phnumber,
            "retrytype": str(retry_mode),
        }
        requests.get(
            settings.SMS_GATEWAY["RESENDPOINT"],
            params=data)
