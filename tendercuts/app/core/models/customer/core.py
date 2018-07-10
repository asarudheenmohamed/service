import itertools

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from app.core.models.store import LocationPincodePincodeStore
from app.core.lib import cache
from app.geohashing.lib.geohash_controller import GeohashController


class FlatAddress(object):
    """Deserialize flat address in user."""

    def __init__(self, address_entity):
        """Initialize the customer Address."""
        self.address = address_entity

    def deserialize(self):
        """Deserialize the address."""
        addresses = []
        for address in self.address:
            address_dict = {'address_id': address.entity_id}
            # Gather all varchars and texts
            eavs = itertools.chain(address.varchars.all(), address.texts.all(), address.ints.all())
            grouper = itertools.groupby(list(eavs), lambda x: x.entity_id)

            for entity_id, group in grouper:
                for eav in group:
                    address_dict[eav.attribute.attribute_code] = eav.value
            
            key_val = cache.generate_prefix_key(
                cache.PREFIX_PINCODE, address_dict.get('postcode'))
            cache_value = cache.get_key(
                key_val, settings.CACHE_DEFAULT_VERSION)
            LocationPincodePincodeStore.objects.filter(
                pincode__pincode=address_dict.get('postcode'))
            if isinstance(cache_value, int) or cache_value is None:

                pin_obj = LocationPincodePincodeStore.objects.filter(
                    pincode__pincode=address_dict.get('postcode'))
                store_id = [
                    obj.store.store_id for obj in pin_obj]
                address_dict['possible_stores'] = store_id

                cache.set_key(key_val, store_id, 60 * 60 *
                              24, settings.CACHE_DEFAULT_VERSION)

            else:
                address_dict['possible_stores'] = cache_value
            
            #store_id for customer address
            address_store_id = None
            if address_dict['geohash'] != None:
                address_store_id = GeohashController().get_store_id(
                    address_dict['geohash'],
                    address_dict['latitude'],
                    address_dict['longitude'])
            
            address_dict['store_id'] = address_store_id

            addresses.append(address_dict)

        return addresses


class FlatCustomer(object):
    """Since django has a stupid EAV architecture, we flattern it out."""

    # prefix used for customer in django tables.
    PREFIX = "u"

    def __init__(self, customer):
        """Initialize the customer object and deserialize.

        Params:
            customer (CustomerEntity) - django model
        """
        self.customer = customer
        self.message = None
        # serialize it immediately.
        self._flat = self.deserialize()

    @property
    def dj_user_id(self):
        """Django user id of the Magento user."""
        return ("{}:{}".format(self.PREFIX, self.customer.entity_id))

    @property
    def entity_id(self):
        """Magento user ID."""
        return self.customer.entity_id

    @property
    def password_hash(self):
        """Return a password hash of user."""
        return self._flat['password_hash']

    @property
    def email(self):
        """Email of the user."""
        return self._flat['email']

    @property
    def mobilenumber(self):
        """Phone of the user."""
        return self._flat['mobilenumber']

    @property
    def firstname(self):
        """Name of the user."""
        return self._flat['firstname']

    def generate_token(self):
        """Create the DRF Token.

        Returns:
         Drf token key

        """
        try:
            user = User.objects.get(username=self.dj_user_id)
        except User.DoesNotExist as e:
            user = User.objects.create_user(
                username=self.dj_user_id)

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def deserialize(self):
        """"Deserialize object by user

        Returns:
         customer deserialize object

        """
        customer = {}

        if self.customer is None:
            return customer

        # Gather all attibute code varchars, ints (billing & shiping)
        eavs = itertools.chain(
            self.customer.varchars.all(),
            self.customer.ints.all())

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create auth token."""
    if created:
        Token.objects.create(user=instance)
