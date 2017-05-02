import abc
import logging

class AbstractGateway:
    def __init__(self, log=None):
        self.log = log or logging.getLogger()

    @abc.abstractmethod
    def check_payment_status(self, orders):
        pass
