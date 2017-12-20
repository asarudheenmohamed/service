import juspay
from django.conf import settings


class JuspayMixin:
    """A mixin to inject all the necessary attributes"""

    @property
    def juspay(self):
        juspay.api_key = settings.PAYMENT['JUSPAY']['id']
        juspay.environment = settings.PAYMENT['JUSPAY']['environment']
        return juspay

    @property
    def return_url(self):
        return settings.PAYMENT['JUSPAY']['return_url']

    @property
    def secret(self):
        return  settings.PAYMENT['JUSPAY']['secret']

    @property
    def merchant_id(self):
        return settings.PAYMENT['JUSPAY']['merchant_id']
