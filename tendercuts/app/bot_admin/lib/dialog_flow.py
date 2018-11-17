import logging
import json

import requests
from django.conf import settings

logger = logging.getLogger()


class DialogFlowQuery(object):
    """Parses the data from flock chat and sends a response
    back to the flock user"""
    QUERY_URL = 'https://api.dialogflow.com/v1/query?v=20170712'

    def __init__(self, chat):
        """
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
        self.chat = chat

    @property
    def headers(self):
        return {
            'Authorization': settings.DIALOG_FLOW['AUTH'],
            'Content-type': 'application/json'
        }

    def _prepare_query(self, chat):
        """@private
        Prepare the data for dialog flow bot

        :return:
        """
        return json.dumps({
            "query": chat['message']['text'],
            "lang": "en",
            "sessionId": chat['message']['from']
        })

    def _prepare_response(self, response):
        """Parse and extract the response from bot

        :param response: {
            "id": "8e439ba3-468c-411e-954d-e929557a621a",
            "timestamp": "2018-11-17T14:07:04.003Z",
            "lang": "en",
            "result": {
                "source": "agent",
                "resolvedQuery": "Where is my orderId #111011",
                "speech": "Can you say that again?",
                "action": "input.unknown",
                "parameters": {},
                "metadata": {
                    "inputContexts": [],
                    "outputContexts": [],
                    "isFallbackIntent": "true",
                    "intentName": "Default Fallback Intent",
                    "intentId": "a44ec421-3406-4873-858d-a2829cccbbcd",
                    "webhookUsed": "false",
                    "webhookForSlotFillingUsed": "false",
                    "contexts": []
                },
                "score": 1
            },
            "status": {
                "code": 200,
                "errorType": "success"
            },
            "sessionId": "u:tbbbgbtz86ub464t"
        }

        :return: (str)

        """
        response = response.json()
        logger.info("Got df response {} ".format(response))
        return response['result']['speech']

    def response(self):
        """
        :param chat(dict): data from flock
        :return:

        """
        data = self._prepare_query(self.chat)

        response = requests.post(
            self.QUERY_URL,
            headers=self.headers,
            data=data
        )

        return self._prepare_response(response)
