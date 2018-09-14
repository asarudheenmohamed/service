import logging

from rest_framework.views import APIView
from app.core.auth import verify_token
from app.store_manager.lib import InventoryFlockMessageController

logger = logging.getLogger()

class FlockAppApi(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    def handle_actions(self, action_data):
        InventoryFlockMessageController().process_action(action_data)

    def post(self, request):
        event_name = self.request.data['name']
        logger.info('GOT {}'.format(self.request.data))

        if event_name not in ['client.flockmlAction']:
            return

        token = request.META.get('X-Flock-Event-Token')
        resp = verify_token(token)

        # TODO clean up code here to handle multiple events
        self.handle_actions(self.request.data)

        return

    def get(self, request):
        return







