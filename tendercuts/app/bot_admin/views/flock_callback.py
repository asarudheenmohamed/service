import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.bot_admin.lib import verify_token, FlockBot, DialogFlowQuery

logger = logging.getLogger()


class FlockAppApi(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    def handle_chat(self, action_data):
        """DEPRECATED: Callback to handle inventory action changes
        ActionId contains the primary key (request-1001)
        """
        from_id = FlockBot.get_sender_id(action_data)
        response = DialogFlowQuery(action_data).response()
        FlockBot().send(from_id, response)
        logger.info(action_data)
        # 0 -? approved, 1- rejected
        # inv_request_id, action = action_data['actionId'].split("-")
        # request = InventoryRequest.objects.get(pk=inv_request_id)
        #
        # req_controller = InventoryRequestController(request)
        # flock_msg_controller = InventoryFlockAppController(request)
        #
        # if request.status != InventoryRequest.Status.CREATED.value:
        #     flock_msg_controller.publish_response('FINISHED')
        #     return
        #
        # if action == '1':
        #     message = ""
        #     req_controller.approve()
        #     flock_msg_controller.publish_response('APPROVED')
        # else:
        #     req_controller.reject(
        #     flock_msg_controller.publish_response('REJECTED')
        pass

    def post(self, request):
        logger.info('GOT {}'.format(self.request.data))
        event_name = self.request.data['name']

        EVENT_CALLBACK_MAP = {
            'chat.receiveMessage': self.handle_chat
        }

        if event_name not in EVENT_CALLBACK_MAP:
            return

        token = request.META.get('X-Flock-Event-Token')
        resp = verify_token(token)

        EVENT_CALLBACK_MAP[event_name](self.request.data)

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
