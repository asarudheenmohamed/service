"""End point for the send sms to the customer mobile number."""
import logging
import requests
import sendotp
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)


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

    def send(self, phnumber, message, scheduled_time=None):
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
            "route": settings.SMS_GATEWAY["ROUTE"],
            "country": settings.SMS_GATEWAY["COUNTRY"],
            "schtime": scheduled_time
        }

        response = requests.get(
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
        logger.debug('Otp send for this number:{}'.format(phnumber))
        otp = self.otp.send(
            phnumber,
            settings.SMS_GATEWAY["SENDER_ID"],
            otp)

        logger.info(
            'Otp sent successfully for this number:{}'.format(phnumber))

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

        logger.debug(
            'Otp send the {} method for this number:{}'.format(
                retry_mode, phnumber))
        requests.get(
            settings.SMS_GATEWAY["RESENDPOINT"],
            params=data)

        logger.info(
            'Otp successfully sent {} method for this number:{}'.format(
                retry_mode, phnumber))

    def send_sms(self, phnumber, message):
        """Send the sms via value first api.

        params:
            phnumber (int): Ph number to send
            message (str): message

        """
        data = {
            "username": settings.VALUE_FIRST_SMS_GATEWAY["USERNAME"],
            "password": settings.VALUE_FIRST_SMS_GATEWAY["PASSWORD"],
            "to": str(phnumber),
            "from": settings.VALUE_FIRST_SMS_GATEWAY["FROM"],
            "text": message
        }

        response = requests.get(settings.VALUE_FIRST_SMS_GATEWAY[
            "ENDPOINT"], params=data)

        return response

    def send_scheduled_sms(self, scheduletime, phnumber, message):
        data = {
            "username": settings.VALUE_FIRST_SMS_GATEWAY["USERNAME"],
            "password": settings.VALUE_FIRST_SMS_GATEWAY["PASSWORD"],
            "to": str(phnumber),
            "scheduletime": scheduletime,
            "action": "UPDATE",
            "guid": settings.VALUE_FIRST_SMS_GATEWAY["GUID"],
            "from": settings.VALUE_FIRST_SMS_GATEWAY["FROM"],
            "text": message
        }

        response = requests.get(settings.VALUE_FIRST_SMS_GATEWAY[
            "ENDPOINT"], params=data)
