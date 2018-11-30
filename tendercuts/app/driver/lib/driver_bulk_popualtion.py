import logging
from app.core import models
from app.core.lib.user_controller import CustomerController
from app.driver.constants import DRIVER_GROUP
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from app.core.models.customer import (CustomerEntity, CustomerEntityVarchar,
                                      FlatCustomer, CustomerAddressEntityVarchar,
                                      CustomerAddressEntityText, CustomerAddressEntity,
                                      CustomerAddressEntityText)


def run(request):
    pass
