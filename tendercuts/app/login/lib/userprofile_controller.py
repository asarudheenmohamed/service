"""Endpoint reset user profile details."""
import hashlib
import logging
import uuid

from django.contrib.auth.models import User

from app.core.models.customer.entity import *
from app.core.models.entity import *

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserProfileEdit:
    """Change user profile details."""

    customer_related_table = {"static": CustomerEntity,
                              "varchar": CustomerEntityVarchar,
                              "datetime": CustomerEntityDatetime,
                              "int": CustomerEntityInt,
                              "text": CustomerEntityText,
                              "decimal": CustomerEntityDecimal}

    def __init__(self, user_id, log):
        """Initialize user id.

        Args:
        user_id(int):customer entity id
        log(obj):log file

        """
        self.entity_id = user_id
        self.logger = log or logger

    def reset_userprofile(self, attribute_code, new_value):
        """Reset userprofile field like static,varchar,datetime,int,decimal.

        Args:
        attribute_code(str):attribute code for user edit field
        new_value(str):user profile edit field value

        Raise:
         If the attribute_code is not available then thrown an error

        """
        eav_obj = EavAttribute.objects.filter(attribute_code=attribute_code)

        try:
            eav_obj = eav_obj[0]
        except IndexError:
            raise ValueError('could not find %s' % (attribute_code))

        cus_model = self.customer_related_table[eav_obj.backend_type]
        if eav_obj.backend_type == "static":
            user_obj = cus_model.objects.filter(
                entity_id=self.entity_id)
            user_obj = user_obj[0]
            user_obj.email = new_value
        else:
            user_obj = cus_model.objects.filter(
                entity_id=self.entity_id,
                attribute_id=eav_obj.attribute_id)
            user_obj = user_obj[0]
            user_obj.value = new_value
        user_obj.save()

        self.logger.info("successfully changed {} for {}".format(
            attribute_code, self.entity_id))

    def reset_password(self, attribute_code, new_password, dry_run=False):
        """Reset user password field.

        Args:
        attribute_code(str):attribute code for user edit field
        new_password(str):new password for the user

        """
        eav_obj = EavAttribute.objects.filter(attribute_code=attribute_code)
        eav_obj = eav_obj[0]
        password_entity = CustomerEntityVarchar.objects.filter(
            entity_id=self.entity_id,
            attribute_id=eav_obj.attribute_id)  # password

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
