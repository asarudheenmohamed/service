from django.conf import settings

import requests

class SMS():
    def __init__(self):
        pass

    def send(self, phnumber, message):

        data = {
            "method": "sms",
            "api_key": settings.SMS_GATEWAY["KEY"],
            "sender": settings.SMS_GATEWAY['SENDER_ID'],
            "to": phnumber,
            "message": message
        }
        print (data)

        resp = requests.post(
                settings.SMS_GATEWAY["ENDPOINT"],
                data=data)
        print(resp.__dict__)

        # Raise error
        resp.raise_for_status()
