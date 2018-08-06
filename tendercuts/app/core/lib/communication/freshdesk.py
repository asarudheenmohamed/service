"""End point for the Fresh desk ticket creation and deletion."""
import json
import logging

import requests
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FreshDesk():
    """Freshdesk Api integrations."""

    def __init__(self):
        pass

    def create_ticket(self, subject, description, email, phone):
        """Create Freshdesk ticket.

        params:
            subject (int): ticket subject
            description (str): ticket discription
            email(str): Customer email
            phone(str): Customer mobile number

        Returns:
            Ticket created objects

        """

        data = {
            "subject": subject,
            "description": description,
            "email": email,
            "priority": settings.FRESHDESK["TICKETS_CREATE"]["PRIORITY"],
            "status": settings.FRESHDESK["TICKETS_CREATE"]["STATUS"],
            "cc_emails": settings.FRESHDESK["CC_EMAILS"],
            "phone": phone,
            "source": settings.FRESHDESK["TICKETS_CREATE"]["SOURCE"],
            "type": settings.FRESHDESK["TICKETS_CREATE"]["TYPE"]
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            settings.FRESHDESK["TICKETS_CREATE"]["ENDPOINT"],
            auth=(settings.FRESHDESK["KEY"],
                  settings.FRESHDESK["PASSWORD"]),
            headers=headers,
            data=json.dumps(data))

        return response

    def delete_fresh_desk_ticket(self, ticket_id):
        """Delete freshdesk ticket.

        Params:
            ticket_id(str): fresh ticket id

        """
        headers = {"Content-Type": "application/json"}

        response = requests.delete(
            settings.FRESHDESK["TICKETS_CREATE"][
                "ENDPOINT"] + '/{}'.format(ticket_id),
            auth=(settings.FRESHDESK["KEY"], settings.FRESHDESK["PASSWORD"]),
            headers=headers)
