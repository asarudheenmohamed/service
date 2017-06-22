"""Endpoint reset user profile details."""
import hashlib
import logging
import uuid

from django.contrib.auth.models import User

from app.core.models.customer.entity import *

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserProfileEdit:
    """Change user profile details."""

    def __init__(self, user_id, log):
        """Initialize user id."""
        self.entity_id = user_id
        self.logger = log or logger

    def reset_email(self, new_email_id):
        """Reset email id field."""
        user_obj = CustomerEntity.objects.filter(
            entity_id=self.entity_id)

        user_obj = user_obj[0]
        user_obj.email = new_email_id
        user_obj.save()

        self.logger.info("successfully changed email for {}".format(
            self.entity_id))

    def reset_username(self, new_user_name):
        """Reset username field."""
        user_obj = CustomerEntityVarchar.objects.filter(
            entity_id=self.entity_id,
            attribute_id=5)

        user_obj = user_obj[0]
        user_obj.value = new_user_name
        user_obj.save()

        self.logger.info("successfully changed username for {}".format(
            self.entity_id))

    def reset_date_of_birth(self, new_dob):
        """Reset date of birth field."""
        user_obj = CustomerEntityDatetime.objects.filter(
            entity=self.entity_id, attribute_id=11)

        user_obj = user_obj[0]
        user_obj.value = new_dob
        user_obj.save()

        self.logger.info("successfully changed date of birth for {}".format(
            self.entity_id))

    def reset_password(self, new_password, dry_run=False):
        """Reset user password field."""
        password_entity = CustomerEntityVarchar.objects.filter(
            entity_id=self.entity_id,
            attribute_id=12)  # password

        if len(password_entity) == 0:
            return
        password_entity = password_entity[0]
        salt = uuid.uuid4().hex

        computed_hash = hashlib.md5(salt + new_password)

        new_password = "{}:{}".format(computed_hash.hexdigest(), salt)
        password_entity.value = new_password

        if not dry_run:
            password_entity.save()
        self.logger.info("successfully changed password for {}".format(
            self.entity_id))
