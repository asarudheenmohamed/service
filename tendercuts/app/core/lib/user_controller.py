"""End point for the controll in user details."""
import hashlib
import random
import string
import uuid
import logging

from django.db.models import Q, Sum, QuerySet
from django.conf import settings

from app.core.lib import cache
from app.core.lib.communication import SMS
from app.core.lib.exceptions import CustomerNotFound, InvalidCredentials
from app.core.models.customer import (CustomerEntity, CustomerEntityVarchar,
                                      FlatCustomer, CustomerAddressEntityVarchar,
                                      CustomerAddressEntityText, CustomerAddressEntity,
                                      CustomerAddressEntityText)

logger = logging.getLogger(__name__)


class CustomerSearchController(object):
    """Static method to find the customer data."""

    @classmethod
    def load_cache_basic_info(cls, entity_id):
        """Return a driver basic information.

        Params:
            entity_id(list): user entity_id

        Returns:
            Returns the basic information from django cache (redis db) if it is avaiable
            otherwise Fetch the data from CustomerEntityVarchar table and updated to django cache.
            Django cache is a temporary storage here we have set 24 hours validation (60*60*24).

        """
        logger.debug(
            'get driver information in django cache for that driver id:{}'.format(
                entity_id))

        # get driver basic info in django cache
        user_details = cache.get_key(
            entity_id, settings.CACHE_DEFAULT_VERSION)

        if not user_details:
            # fetch drive information from CustomerEntityVarchar model.
            logger.debug(
                "fetch user information in CustomerEntityVarchar model:{}".format(
                    entity_id))

            load_basic_info = cls.load_basic_info(entity_id)
            user_details = {
                'entity_id': load_basic_info[0],
                'email': load_basic_info[1],
                'phone': load_basic_info[2],
                'name': load_basic_info[3]
            }
            cache.set_key(load_basic_info[0], user_details, 60 * 60 *
                          24, settings.CACHE_DEFAULT_VERSION)
            logger.info(
                "get user information for the given entity id:{}".format(
                    entity_id))

        return user_details

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
        varchar_objects = CustomerEntityVarchar.objects.filter(
            attribute_id__in=[
                149, 5], entity_id=user_id).prefetch_related('entity__reward_point')

        query_set = varchar_objects.order_by(
            '-attribute_id').values_list('entity', 'entity__email', 'value')

        if not query_set:
            raise CustomerNotFound(
                "No data found for customer: {}".format(user_id))

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
            "addresses__texts", "addresses__texts__attribute",
            "addresses__ints", "addresses__ints__attribute")
        if not customers:
            raise CustomerNotFound

        obj = FlatCustomer(customers[0])

        return obj

    @classmethod
    def get_django_username(cls, phone_number):
        """Get Django username from user phone number.

        Params:
            phone_number: User phone number.

        Returns:
            Django username

        """
        try:
            customer = CustomerEntityVarchar.objects.filter(
                Q(attribute_id=149) & (Q(value=phone_number) | Q(entity__email=phone_number)))[0]
        except:
            raise CustomerNotFound()

        return ("{}:{}".format("u", customer.entity_id))


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


class CustomerAddressController(object):

    address = None  # type: CustomerAddressEntity

    def __init__(self, address):
        self.address = address

    @property
    def geohash_field(self):
        return settings.MAGE_ATTRS['GEOHASH']

    @property
    def lat_field(self):
        return settings.MAGE_ATTRS['LATITUDE']

    @property
    def lng_field(self):
        return settings.MAGE_ATTRS['LONGITUDE']

    @property
    def street_field(self):
        return settings.MAGE_ATTRS['STREET']

    @property
    def address_id(self):
        return self.address.entity_id

    def update_address(self, lat, lng, geohash, street):
        varchars = CustomerAddressEntityVarchar.objects.all()
        import pdb
        pdb.set_trace()
        geohash_row = varchars.filter(
            entity_id=self.address_id, attribute_id=self.geohash_field).first()
        geohash_row.value = geohash
        geohash_row.save()

        lat_row = varchars.filter(
            entity=self.address_id, attribute=self.lat_field).first()
        lat_row.value = lat
        lat_row.save()

        lng_row = varchars.filter(
            entity=self.address_id, attribute=self.lng_field).first()
        lng_row.value = lng
        lng_row.save()

        texts = CustomerAddressEntityText.objects
        street_row = texts.filter(
            entity=self.address_id, attribute=self.street_field).first()  # type: CustomerAddressEntityText

        components = street_row.value.split('\n')  # type: list
        if len(components) < 2:
            components.append(street)
        else:
            components[1] = street

        street_row.value = "\n".join(components)
        street_row.save()
