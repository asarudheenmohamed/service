from django.conf import settings

import requests

class Flock():
    
    #USER_TOKEN = "30b4de1e-bc62-4165-ad84-601f33e4c68e"
    # Minion
    USER_TOKEN = "a5e7f77b-a005-4134-affa-3a01da13cb42"

    #https://api.flock.co/v1/groups.list?token=30b4de1e-bc62-4165-ad84-601f33e4c68e
    GROUPS = {
        "TECH_SUPPORT": "g:5282d2270ce34879981964619491b654",
        "SCRUM": "g:5db92fa6225149be84183e4d79c19ada",
    }

    def __init__(self):
        pass

    def send(self, group_name, message):
        url = "https://api.flock.co/v1/chat.sendMessage?to={}&text={}&token={}".format(
            self.GROUPS[group_name],
            message,
            self.USER_TOKEN)

        resp = requests.get(url)

        # Raise error
        resp.raise_for_status()
