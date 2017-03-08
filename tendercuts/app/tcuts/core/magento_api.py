import magento
import logging

class Connector:
    def __init__(self, test=True):
        if test:
            logging.info("Connecting to TEST SERVER")

        self.api = magento.MagentoAPI(
                 "tendercuts.in" if not test else "staging.tendercuts.in",
                 443,
                 "admin",
                 "Tendercuts123!",
                 path="/index.php/api/xmlrpc/" if not test else  "/v2/index.php/api/xmlrpc/",
                 allow_none=True,
                 proto='https')

        #self.api = magento.MagentoAPI(
        #    "localhost",
        #    80, "admin", "Tendercuts123!",
        #    path="/tendercuts-site/index.php/api/xmlrpc/",
        #    allow_none=True)

