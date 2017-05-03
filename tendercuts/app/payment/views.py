from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
from .lib import gateway as gw


class SimplClaimTxnApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """

    def post(self, request, format=None):
        """
        """
        increment_id = self.request.data['increment_id']
        token = self.request.data['token']

        simpl = gw.GetSimplGateway()
        status = simpl.update_order_with_payment(
            increment_id,
            token)

        return Response({"status": status})
