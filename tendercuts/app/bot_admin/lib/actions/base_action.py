class BaseAction(object):
    """Base class for handling the webhook messages"""

    def __init__(self, data):
        """
        data = {
         u'queryResult': {
            u'fulfillmentMessages': [{
                u'text': {u'text': [u'']}
            }],
            u'allRequiredParamsPresent': True,
            u'parameters': {
                u'orderId ': {u'orderId': 700109219.0}
            },
            u'languageCode': u'en',
            u'intentDetectionConfidence': 1.0,
            u'intent': {
                u'displayName': u'Order Status',
                u'name': u'projects / tendercuts - d9c26 / agent / intents / bf6e 34cd - 1c2f - 40a7 - a832 - b07216defb9b'},
            u'queryText': u'# 700109219'},
            u'originalDetectIntentRequest ': {},
            u'session': u' projects / tendercuts - d9c26 / agent / sessions / u: tbbbgbtz86ub464t',
            u'responseId ': u'46dc744e - dc1f - 47c5 - bbb3 - cefa166d0e09'}

        """
        self._data = data

    @property
    def params(self):
        return self._data['queryResult']['parameters']
