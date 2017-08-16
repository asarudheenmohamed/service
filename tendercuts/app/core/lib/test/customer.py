"""Utilies for Test app."""

import random
import uuid

from rest_framework.test import APIClient
from django.contrib.auth.models import User

from app.core.lib import magento


def generate_customer(
        firstname=None,
        lastname=None,
        mobilenumber=None,
        email=None,
        group_id=None):
    """Generate a mock customer."""
    firstnames = ["John", "Dave", "Sarah", "David"]
    lastnames = ["Appleseed", "Chapelle", "Silverman", "Schumer"]

    data = {
        "mobilenumber": mobilenumber or random.randint(1000000000, 2000000000),
        "firstname": firstname or random.choice(firstnames),
        "lastname": lastname or random.choice(lastnames),
        "email": email or "{}@email.com".format(uuid.uuid4()),
        "password": "12345678",
        "website_id": 1,
        "store_id": 1,
        "group_id": group_id or 1
    }

    mage = magento.Connector()
    data['entity_id'] = mage.api.customer.create(data)

    return data


def auth_client(customer):
    """For the given customer create a auth_client"""
    # A bloody hack to ensure that the user is created in DJ.
    customer.generate_token()

    user = User.objects.get(username=customer.dj_user_id)
    client = APIClient()
    client.force_authenticate(user=user)

    return client
