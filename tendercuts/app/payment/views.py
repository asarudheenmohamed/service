from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
from .lib import gateway as gw


class VerifyTransaction(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    GW_MAP = {
        "getsimpl": gw.GetSimplGateway,
        "juspay": gw.JusPayGateway,
        "razorpay": gw.RzpGateway
    }

    def post(self, request, format=None):
        """
        Check the gw code and trigger the appropriate gw action.
        """
        increment_id = self.request.data['increment_id']
        vendor_id = self.request.data.get('vendor_id', None)
        gateway = self.request.data.get('gw', None)

        if gateway not in self.GW_MAP:
            raise exceptions.ValidationError(('Invalid data'))

        gateway = self.GW_MAP[gateway](log=logger)
        status = gateway.verify_transaction(order_id=increment_id, vendor_id=vendor_id)
        logger.info("Sending back {} for the transaction {}".format(status, vendor_id))
        return Response({"status": status})
