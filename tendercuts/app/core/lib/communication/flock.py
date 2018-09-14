"""End point for the send flock message to the store groups."""
import json

import requests
from django.conf import settings


class Flock():
    """To send the flock message."""

    # USER_TOKEN = "30b4de1e-bc62-4165-ad84-601f33e4c68e"
    # Minion
    USER_TOKEN = "a5e7f77b-a005-4134-affa-3a01da13cb42"

    # https://api.flock.co/v1/groups.list?token=30b4de1e-bc62-4165-ad84-601f33e4c68e

    def __init__(self):
        """constructor."""
        pass

    def send(self, group_name, message):
        """Send flock message.

        params:
            group_name (unicode): group token
            message (str): message

        raises:
            Error in case of bad/invalid request

        """
        url = "https://api.flock.co/v1/chat.sendMessage?to={}&text={}&token={}".format(
            settings.GROUPS[group_name],
            message,
            self.USER_TOKEN)

        resp = requests.get(url)

        resp.raise_for_status()

    def send_flockml(self, group_name, products, title, description, send_as=None):
        """Send flockml message.

        params:
            group_name (unicode): group token
            products (str): products
            title (str): title
            description(str): description

        raises:
            Error in case of bad/invalid request

        """
        data = {
                "token": self.USER_TOKEN,
                "to": settings.GROUPS[group_name],
                "attachments": [
                    {
                        "title": title,
                        "description": description,
                        "views": {
                            "flockml": products
                        }
                    }
                ]
            }

        if send_as:
            data['sendAs'] = {'name': send_as}

        resp = requests.post(
        "https://api.flock.co/v1/chat.sendMessage/", data=json.dumps(data))

        # Raise error
        resp.raise_for_status()
