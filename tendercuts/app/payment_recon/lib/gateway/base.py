import abc

class AbstractGateway:
    def __init__(self):
        pass

    @abc.abstractmethod
    def check_payment_status(self, orders):
        pass
