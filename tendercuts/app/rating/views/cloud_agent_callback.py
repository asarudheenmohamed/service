"""Endpoint to the created a freshdesk attachment ticket creation CloudAgent callback details for the customer."""

from app.rating import tasks
from rest_framework import status, viewsets
from rest_framework.response import Response


class CloudAgentCallback(viewsets.GenericViewSet):
    """Endpoint to freshdesk attachment ticket creation.

    EndPoint:
        API: rating/callback/
    """
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """CloudAgent callback  endpoint.

        Params:
            CloudAgent Callback details

        returns:
            Response({status: bool, message: str})

        """

        data = request.data.copy()

        tasks.create_fresh_desk_attachment_ticket.delay(data)

        return Response(status=status.HTTP_201_CREATED)
