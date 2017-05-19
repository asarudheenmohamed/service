from .entity import *
import itertools
import itertools
import sys
import hashlib
import hashlib
import uuid

from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.db.models import Q
from .core import *


class AuthenticationException(Exception):
    pass


class CustomerNotFound(AuthenticationException):
    pass


class InvalidCredentials(AuthenticationException):
    pass


class FlatAddress():

    def __init__(self, address_entity):
        self.address = address_entity

    def deserialize(self):

        addresses = []
        for address in self.address:

            address_dict = {'address_id': address.entity_id}
            # Gather all varchars and texts
            eavs = itertools.chain(address.varchars.all(), address.texts.all())
            grouper = itertools.groupby(list(eavs), lambda x: x.entity_id)

            for entity_id, group in grouper:
                for eav in group:
                    address_dict[eav.attribute.attribute_code] = eav.value

            addresses.append(address_dict)
        return addresses


class FlatCustomer():
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

        return cls.load_by_id(customer.entity_id)

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates the user

        Args:
            username (str): username
            password (str): password

        Returns:
            User 
        """

        user = cls.load_by_phone_mail(username)
        if not user.validate_password(password):
            raise InvalidCredentials

        return user

    @classmethod
    def load_by_id(cls, customer_id):
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

    def __init__(self, customer):
        self.customer = customer
        self.message = None
        self._flat = self.deserialize()

    @property
    def dj_user_id(self):
        """
        Django user id of the Magento user
        """
        return ("{}:{}".format(self.PREFIX, self.customer.entity_id))

    def generate_token(self):
        """
        """
        try:
            user = User.objects.get(username=self.dj_user_id)
        except User.DoesNotExist as e:
            user = User.objects.create_user(
                username=self.dj_user_id)

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def deserialize(self):
        customer = {}

        if self.customer is None:
            return customer

        # Gather all attibute code varchars
        eavs = itertools.chain(self.customer.varchars.all())

        grouper = itertools.groupby(list(eavs), lambda x: x.entity_id)
        for entity_id, group in grouper:
            for eav in group:
                customer[eav.attribute.attribute_code] = eav.value

        customer['address'] = FlatAddress(
            self.customer.addresses.all()).deserialize()
        customer['email'] = self.customer.email
        customer['message'] = self.message
        customer['entity_id'] = self.customer.entity_id

        try:
            reward_pts_sum = self.customer.reward_point.filter(is_expired=0) \
                .aggregate(amount=Sum('amount'))
            customer['reward_points'] = reward_pts_sum['amount'] or 0
        except Exception as e:
            customer['reward_points'] = 0

        try:
            customer['store_credit'] = \
                self.customer.store_credit.all()[0].amount
        except Exception as e:
            customer['store_credit'] = 0

        customer['token'] = self.generate_token()

        return customer

    def validate_password(self, password):
        password_hash = self._flat['password_hash']

        salts = password_hash.split(":")

        if len(salts) == 1:
            return self.user.password == hashlib.md5(password).hexdigest()

        salted_hash, salt = salts
        computed_hash = hashlib.md5(salt + password)

        return computed_hash.hexdigest() == salted_hash

    def reset_password(self, new_password, dry_run=False):
        password_entity = CustomerEntityVarchar.objects.filter(
            entity_id=self.customer.entity_id,
            attribute_id=12)

        if len(password_entity) == 0:
            return

        password_entity = password_entity[0]
        salt = uuid.uuid4().hex

        computed_hash = hashlib.md5(salt + new_password)

        new_password = "{}:{}".format(computed_hash.hexdigest(), salt)
        password_entity.value = new_password

        if not dry_run:
            password_entity.save()


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
