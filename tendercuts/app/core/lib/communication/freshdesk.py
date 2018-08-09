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
            "priority": settings.FRESHDESK["TICKETS_CREATE"]["PRIORITY"]["HIGH"],
            "status": settings.FRESHDESK["TICKETS_CREATE"]["STATUS"]["OPEN"],
            "cc_emails": settings.FRESHDESK["CC_EMAILS"],
            "phone": str(phone),
            "source": settings.FRESHDESK["TICKETS_CREATE"]["SOURCE"]["PORTAL"],
            "type": settings.FRESHDESK["TICKETS_CREATE"]["TYPE"],
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            settings.FRESHDESK["TICKETS_CREATE"]["ENDPOINT"],
            auth=(settings.FRESHDESK["KEY"],
                  settings.FRESHDESK["PASSWORD"]),
            headers=headers,
            data=json.dumps(data))

        return response

    def create_ticket_attachment(
            self, attachment, subject, description, phone, type_, answered_agent, disposition, commends):
        """Create Freshdesk attachment ticket.

        params:
            attachment(file): attachment
            subject (int): ticket subject
            description (str): ticket discription
            email(str): Customer email
            phone(str): Customer mobile number

        Returns:
            Ticket attachment created objects

        """

        multipart_data = {
            'subject': (None, subject),
            "phone": (None, str(phone)),
            "name": (None, str(phone)),
            'description': (None, description),
            'status': (None, str(settings.FRESHDESK["TICKETS_CREATE"]["STATUS"]["CLOSED"])),
            'priority': (None, str(settings.FRESHDESK["TICKETS_CREATE"]["PRIORITY"]["LOW"])),
            'custom_fields[cf_disposition]': (None, disposition),
            'custom_fields[voc]': (None, commends),
            'custom_fields[cf_answered_agent]': (None, answered_agent),
            'type': (None, str(type_)),
            "source": (None, str(settings.FRESHDESK["TICKETS_CREATE"]["SOURCE"]["PHONE"]))
        }
        if attachment:
            multipart_data['attachments[]'] = open(attachment, 'rb')

        response = requests.post(
            settings.FRESHDESK["TICKETS_CREATE"]["ENDPOINT"],
            auth=(settings.FRESHDESK["KEY"],
                  settings.FRESHDESK["PASSWORD"]),
            files=multipart_data,
        )

        logger.info(
            'Created Freshdesk desk attachment ticket for the customer:{}'.format(phone))

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
