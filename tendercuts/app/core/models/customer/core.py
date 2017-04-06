from .entity import *
import itertools
import itertools
import sys
import hashlib

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

            address_dict = {}
            eavs = itertools.chain(address.varchars.all(), address.texts.all())
            grouper = itertools.groupby(list(eavs), lambda x: x.entity_id)

            for entity_id, group in grouper:
                for eav in group:
                    address_dict[eav.attribute.attribute_code] = eav.value

            addresses.append(address_dict)
        return addresses


class FlatCustomer():

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
        customers = CustomerEntity.objects.filter(entity_id=customer_id).prefetch_related(
            "reward_point",
            "varchars", "varchars__attribute",
            "addresses", "addresses__varchars", "addresses__varchars__attribute",
            "addresses__texts", "addresses__texts__attribute")

        return cls(customers[0])

    def __init__(self, customer):
        self.customer = customer
        self.message = None
        self._flat = self.deserialize()

    def deserialize(self):
        customer = {}

        if self.customer is None:
            return customer

        eavs = itertools.chain(self.customer.varchars.all())

        grouper = itertools.groupby(list(eavs), lambda x: x.entity_id)
        for entity_id, group in grouper:
            for eav in group:
                customer[eav.attribute.attribute_code] = eav.value

        customer['address'] = FlatAddress(
            self.customer.addresses.all()).deserialize()
        customer['email'] = self.customer.email
        customer['message'] = self.message
        customer['reward_points'] = \
            self.customer.reward_point.all()[0].point_balance

        return customer

    def validate_password(self, password):
        password_hash = self._flat['password_hash']

        salts = password_hash.split(":")

        if len(salts) == 1:
            return self.user.password == hashlib.md5(password).hexdigest()

        salted_hash, salt = salts
        computed_hash = hashlib.md5(salt + password)

        return computed_hash.hexdigest() == salted_hash
