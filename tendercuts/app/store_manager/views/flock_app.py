from rest_framework.views import APIView
from app.core.auth import verify_token

class FlockAppApi(APIView):
    """
    This viewset automatically provides `list` and `detail` actions.

    Enpoint to provide a list for sales orders
    """
    # Opening the endpoint for anonymous browsing
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        event_name = self.request.data['name']

        if event_name not in ['client.flockmlAction']:
            return

        token = request.META.get('X-Flock-Event-Token')
        resp = verify_token(token)





