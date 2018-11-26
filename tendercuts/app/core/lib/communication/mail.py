import requests
import json
from django.conf import settings


class Mail:
    def send(self, sender, receivers, subject, message, files=None):
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            'Authorization': "Bearer {}".format(settings.MAIL_GATEWAY['KEY']),
            'content-type': 'application/json'
        }
        to = [{"email": receiver} for receiver in receivers]

        data = {
            "personalizations": [
                {
                    "to": to,
                    "subject": subject
                }
            ],
            "from": {
                "email": sender
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": message
                }
            ]
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp.raise_for_status()

