from ... import models as models


class ShadowFaxResponse(object):

    def __init__(self, data):
        self._data = data

    @property
    def rider_name(self):
        return None

    @property
    def rider_contact(self):
        return None

    def to_model(self):
        sfx_update = models.ShadowFaxUpdates()
        sfx_update.sfx_order_id = self.sfx_order_id
        sfx_update.client_order_id = self.client_order_id
        sfx_update.order_status = self.status
        sfx_update.rider_contact = self.rider_contact
        sfx_update.rider_name = self.rider_name

        return sfx_update



class ShadowFaxCreateResponse(ShadowFaxResponse):
    @property
    def sfx_order_id(self):
        return self._data['data']['sfx_order_id']

    @property
    def client_order_id(self):
        return self._data['data']['order_details']['client_order_id']

    @property
    def status(self):
        return self._data['data']['status']


class ShadowFaxDriverCallbackResponse(ShadowFaxResponse):
    @property
    def sfx_order_id(self):
        return self._data['sfx_order_id']

    @property
    def client_order_id(self):
        return self._data['client_order_id']

    @property
    def status(self):
        return self._data['order_status']

    @property
    def rider_name(self):
        return self._data['rider_name']

    @property
    def rider_contact(self):
        return self._data['rider_contact']
