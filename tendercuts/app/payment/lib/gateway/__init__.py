from .payu import Payu
from .paytm import PaytmGateway
from .simpl import GetSimplGateway
from .rzp import RzpGateway
from .juspay import JusPayGateway, JuspayTransaction


def get_gateway_by_method(method):
    """Get the gateway class by the magento method name."""
    gateway = {
        "payubiz": Payu,
        "paytm": PaytmGateway,
        "juspay": JusPayGateway,
        "simpl": GetSimplGateway
    }

    try:
        return gateway[method]
    except KeyError:
        raise ValueError("Invalid payment method: {}".format(method))

