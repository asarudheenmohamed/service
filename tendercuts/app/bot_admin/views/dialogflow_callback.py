import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.bot_admin.auth import AdminPermission

logger = logging.getLogger()


class DialogFlowAppApi(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    permission_classes = (AdminPermission,)

    def post(self, request):
        logger.info('DF DATA {}'.format(self.request.data))
        # event_name = self.request.data['name']
        #
        # EVENT_CALLBACK_MAP = {
        #     'chat.receiveMessage': self.handle_chat
        # }
        #
        # if event_name not in EVENT_CALLBACK_MAP:
        #     return
        #
        # token = request.META.get('X-Flock-Event-Token')
        # resp = verify_token(token)
        #
        # EVENT_CALLBACK_MAP[event_name](self.request.data)

        response = {
            "fulfillmentText": "This is a text response",
            "source": "api1.tendercuts.in",
        }

        return Response(response, status=status.HTTP_200_OK)
