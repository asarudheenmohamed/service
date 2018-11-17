"""End point for the send flock message to the store groups."""

import requests


class FlockBot():
    """To send the flock message."""
    APP_TOKEN = "edbdcc62-e9d0-4742-80d5-7d96ed2d832d"

    @classmethod
    def get_sender_id(cls, chat):
        """Helper to get the senderId
        :param chat: dict
        {
            u'message': {
                u'onBehalfOf': u'',
                u'from': u'u:tbbbgbtz86ub464t',
                u'uid': u'1542462841594-XXo-m203',
                u'timestamp': u'2018-11-17T13:54:01.594Z',
                u'to': u'u:B66bmb36ebbh2om5',
                u'text': u'hi',
                u'visibleTo': [],
                u'id': u'd_1542462840570_vjz2t7gj',
                u'timestampInMillis': 1542462841594},
            u'userId': u'u:tbbbgbtz86ub464t',
            u'name': u'chat.receiveMessage'}

        """
        return chat['from']

    def send(self, user_id, message):
        """Send flock message.

        params:
            group_name (unicode): group token
            message (str): message

        raises:
            Error in case of bad/invalid request

        """
        url = "https://api.flock.co/v1/chat.sendMessage?to={}&text={}&token={}".format(
            user_id,
            message,
            self.APP_TOKEN)

        resp = requests.get(url)

        resp.raise_for_status()
