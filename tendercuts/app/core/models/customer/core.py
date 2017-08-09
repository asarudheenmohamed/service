import itertools

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
            eavs = itertools.chain(address.varchars.all(), address.texts.all())
            grouper = itertools.groupby(list(eavs), lambda x: x.entity_id)

            for entity_id, group in grouper:
                for eav in group:
                    address_dict[eav.attribute.attribute_code] = eav.value

            addresses.append(address_dict)
        return addresses


class FlatCustomer(object):
    """A dirty way of serilizing, ideally need to move DRF."""

    # prefix used for customer in django tables.
    PREFIX = "u"

    def __init__(self, customer):
        """Initialize the customer object and deserialize."""
        self.customer = customer
        self.message = None
        self._flat = self.deserialize()

    @property
    def dj_user_id(self):
        """Django user id of the Magento user."""
        return ("{}:{}".format(self.PREFIX, self.customer.entity_id))

    def password_hash(self):
        """return a password hash by user."""
        return self._flat['password_hash']

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create auth token."""
    if created:
        Token.objects.create(user=instance)
