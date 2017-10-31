"""End point for the controll in user details."""
import hashlib
import random
import string
import uuid

from django.db.models import Q

from app.core.lib import cache
from app.core.lib.communication import SMS
from app.core.lib.exceptions import CustomerNotFound, InvalidCredentials
from app.core.models.customer import (CustomerEntity, CustomerEntityVarchar,
                                      FlatCustomer)


class CustomerSearchController(object):
    """Static method to find the customer data."""

    @classmethod
    def load_basic_info(cls, user_id):
        """Yet another convenience method.

        this one load the very basic info
        of the customer such as ph numbver or mail.

        Args:
         user_id(int):user id

        Returns:
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
        """Check user exist."""
        query_set = CustomerEntityVarchar.objects.filter(
            Q(attribute_id=149) & (Q(value=username) | Q(entity__email=username)))

        if len(query_set) == 0:
            return False

        return True

    @classmethod
    def load_by_phone_mail(cls, username):
        """Load the customer object by email or phone number.

        Wrapper on top of by id.
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
                "ints", "ints__attribute",
                "addresses", "addresses__varchars",
                "addresses__varchars__attribute",
                "addresses__texts", "addresses__texts__attribute")

        if not customers:
            raise CustomerNotFound

        obj = FlatCustomer(customers[0])

        return obj


class CustomerController(object):
    """Customer credentials controller."""

    def __init__(self, customer):
        """Initialize the customer object.

        Params:
            customer(FlatCustomer) - Customer obj to wrap
        """
        self.customer = customer

    @classmethod
    def verify_with_otp(self, username):
        """Check whether the mobile number is verified or not in redis db.

        Params:
         username(int): customer mobile number

        returns:
            redis value

        """
        redis_value = cache.get_key(username)
        if redis_value not in ['verified']:
            raise InvalidCredentials

        return redis_value

    def authenticate_with_password(self, username, password):
        """Check whether the given password is  Valid or not.

        Params:
         username(int): customer mobile number
         password: customer entered password

        """
        if not self.validate_password(password):
            raise InvalidCredentials

    @classmethod
    def authenticate(cls, username, password, otp_mode=False):
        """Authenticate the user in 2 modes - otp & user/pass.

        If otp_mode is specified
            username will be mobile number
            password will be empty
            We verify the user based on the verified key in redis.

        Args:
            username (str): username
            password (str|None): password
            otp_mode(bool): default to False, otp via login or not

        Returns:
            User

        """
        user = CustomerSearchController.load_by_phone_mail(username)

        if otp_mode:
            redis_value = cls.verify_with_otp(username)
        else:
            cls(user).authenticate_with_password(username, password)

        return user

    def generate_random_password(self):
        """Generate a random password."""
        random_pass = ''.join(
            [random.choice(string.ascii_lowercase) for n in xrange(5)])
        random_pass += str(random.randint(0, 9))
        return random_pass

    def generate_and_reset_password(self, mobile):
        """Generate password and send password to customer mobile number.

        params:
         mobile(int): customer mobile number

        """
        # check if user verified
        self.verify_with_otp(mobile)
        # generate new password
        new_password = self.generate_random_password()
        # reset customer password
        self.reset_password(new_password)
        msg = ("""Your request for password reset is now successful. New password: {}""").format(
            new_password)
        # send password to customer mobile number
        SMS().send(phnumber=mobile, message=msg)

    def validate_password(self, input_password):
        """Validate user password.

        Params:
            input_password (str): Password entered by user.

        Returns:
            True or false

        """
        salts = self.customer.password_hash.split(":")
        if len(salts) == 1:
            return self.customer.password_hash == hashlib.md5(
                input_password).hexdigest()

        salted_hash, salt = salts
        computed_hash = hashlib.md5(salt + input_password)
        return computed_hash.hexdigest() == salted_hash

    def reset_password(self, new_password, dry_run=False):
        """Reset user password.

        Params:
            new_password(str): New password.

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
