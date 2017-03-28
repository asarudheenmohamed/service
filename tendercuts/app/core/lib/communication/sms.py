from django.conf import settings

import requests

class SMS():
    def __init__(self):
        pass

    def send(self, phnumber, message):

        data = {
            "workingkey": settings.SMS_GATEWAY["KEY"],
            "sender": settings.SMS_GATEWAY['SENDER_ID'],
            "to": phnumber,
            "message": message
        }

        resp = requests.post(
                settings.SMS_GATEWAY["ENDPOINT"],
                data=data,
                timeout=30)

        # Raise error
        resp.raise_for_status()
