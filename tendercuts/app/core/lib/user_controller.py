from app.core.models.entity import *
import itertools
import sys
import hashlib
import uuid
import redis
from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.db.models import Q
from app.core.models.customer.core import *

from .. import models


class AuthenticationException(Exception):
    pass


class CustomerNotFound(AuthenticationException):
    pass


class InvalidCredentials(AuthenticationException):
    pass


class CustomerSearchController:
    """
    A dirty way of serilizing, ideally need to move DRF
    """

    # prefix used for customer in django tables.
    PREFIX = "u"

    @classmethod
    def load_basic_info(cls, user_id):
        """
        Yet another convenience method, this one load the very basic info
        of the customer such as ph numbver or mail

        returns:
            A tuple of (userid, email, phone, name)
        """
        query_set = CustomerEntityVarchar.objects                 \
            .filter(attribute_id__in=[149, 5], entity_id=user_id) \
            .order_by('-attribute_id')                             \
            .values_list('entity', 'entity__email', 'value')

        if not query_set:
            raise CustomerNotFound

        flattened_data = []
        flattened_data.extend(query_set[0])
        # merge the name attribute also
        # first row second col
        flattened_data.append(query_set[1][2])

        return flattened_data

    @classmethod
    def is_user_exists(cls, username):
        """
        TODO: NEEDS to be rewritten
        """
        query_set = CustomerEntityVarchar.objects.filter(
            Q(attribute_id=149) & (Q(value=username) | Q(entity__email=username)))

        if len(query_set) == 0:
            return False

        return True

    @classmethod
    def load_by_phone_mail(cls, username):
        """Load the customer object by email or phone number. Wrapper on top
        of by id.

        Args:
            username (str): Email/PH

        Returns:
            customer.Customer

        Raises:
            CustomerNotFound: If no customer is found
        """

        query_set = CustomerEntityVarchar.objects.filter(
            Q(attribute_id=149) & (Q(value=username) | Q(entity__email=username)))

        if len(query_set) == 0:
            raise CustomerNotFound()

        customer = query_set[0]

        return CustomerController.load_by_id(customer.entity_id)


class CustomerController:

    def __init__(self, customer):
        # a = models.FlatCustomer(customer)
        self.customer = customer
        self.message = None
        self._flat = self.deserialize()

    @classmethod
    def authenticate_otp(cls, username, password, otp_mode):
        """Authenticates the user otp via and password

        Args:
            username (str): username
            password (str): password
            otp_mode(bol):otp via login or not

        Returns:
            User
        """
        user = CustomerSearchController.load_by_phone_mail(username)

        if otp_mode:
            redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
            a = models.OtpList.redis_key_based_get(
                redis_db, username)

            if a not in ['verified']:
                raise ValueError

        else:
            if not user.validate_password(password):
                raise InvalidCredentials

        return user

    @classmethod
    def load_by_id(cls, customer_id):
        """Load the customer object by id.

        Args:
            custemer_id(int):user id

        Returns:
            user object
        """
        customers = CustomerEntity.objects.filter(entity_id=customer_id) \
            .prefetch_related(
                "reward_point", "store_credit",
                "varchars", "varchars__attribute",
                "addresses", "addresses__varchars",
                "addresses__varchars__attribute",
                "addresses__texts", "addresses__texts__attribute")

        if not customers:
            raise CustomerNotFound

        return cls(customers[0])

    def validate_password(self, password):
        """Validate user password.

        Args:
         password:user pasword

        Returns:
            True or false

        """
        password_hash = self._flat['password_hash']

        salts = password_hash.split(":")

        if len(salts) == 1:
            return self.user.password == hashlib.md5(password).hexdigest()

        salted_hash, salt = salts
        computed_hash = hashlib.md5(salt + password)

        return computed_hash.hexdigest() == salted_hash

    def reset_password(self, new_password, dry_run=False):
        """Reset user password.

        Args:
         new_passwrd:use new password

        """
        password_entity = CustomerEntityVarchar.objects.filter(
            entity_id=self.customer.entity_id,
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

    def deserialize(self):
        """Deserialize obj in user"""
        obj = models.FlatCustomer(self.customer)
        return obj.deserialize()
