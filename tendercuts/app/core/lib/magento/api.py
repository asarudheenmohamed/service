from django.conf import settings
import magento
import logging


class Connector:
    def __init__(self, test=True):
        if test:
            logging.info("Connecting to TEST SERVER")

        self.api = magento.MagentoAPI(
            settings.MAGENTO["url"],
            settings.MAGENTO["port"],
            settings.MAGENTO["username"],
            settings.MAGENTO["password"],
            path=settings.MAGENTO["endpoint"],
            allow_none=True,
            proto=settings.MAGENTO["proto"])
