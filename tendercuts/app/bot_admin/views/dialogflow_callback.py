import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.bot_admin.auth import AdminPermission
from ..lib import actions

logger = logging.getLogger()


class DialogFlowAppApi(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    permission_classes = (AdminPermission,)

    def post(self, request):
        logger.info('DF DATA {}'.format(self.request.data))
        data = self.request.data
        event_name = data['queryResult']['intent']['displayName']

        CALLBACK_MAP = {
            'ORDER_CANCELLED': actions.CancelOrderAction,
            'ORDER_COMPLETED': actions.CompleteOrderAction,
            'ORDER_STATUS': actions.OrderStatusAction
        }

        response = {
            "fulfillmentText": "No action found for this, please check with Tech Support.",
            "source": "api1.tendercuts.in",
        }

        if event_name not in CALLBACK_MAP:
            return Response(response, status=status.HTTP_200_OK)

        action = CALLBACK_MAP[event_name]
        response_text = action(data).execute()

        response.update({
            "fulfillmentText": response_text
        })

        return Response(response, status=status.HTTP_200_OK)







