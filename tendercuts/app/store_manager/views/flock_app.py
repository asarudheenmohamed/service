import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.core.auth import verify_token
from app.store_manager.lib import InventoryFlockAppController
from app.inventory.lib import InventoryController, InventoryRequestController
from app.inventory.models import InventoryRequest

logger = logging.getLogger()

class FlockAppApi(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    def handle_inventory_action(self, action_data):
        """Callback to handle inventory action changes
        ActionId contains the primary key (request-1001)
        """
        # 0 -? approved, 1- rejected
        inv_request_id, action = action_data['actionId'].split("-")
        request = InventoryRequest.objects.get(pk=inv_request_id)

        req_controller = InventoryRequestController(request)
        flock_msg_controller = InventoryFlockAppController(request)

        if request.status != InventoryRequest.Status.CREATED.value:
            flock_msg_controller.publish_response('FINISHED')
            return

        if action == '1':
            message = ""
            req_controller.approve()
            flock_msg_controller.publish_response('APPROVED')
        else:
            req_controller.reject()
            flock_msg_controller.publish_response('REJECTED')


    def post(self, request):
        logger.info('GOT {}'.format(self.request.data))
        event_name = self.request.data['name']

        if event_name not in ['client.flockmlAction']:
            return Response(status=status.HTTP_200_OK)

        token = request.META.get('X-Flock-Event-Token')
        resp = verify_token(token)

        # TODO clean up code here to handle multiple events
        self.handle_inventory_action(self.request.data)

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)







