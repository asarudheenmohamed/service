import rest_framework.authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from .. import models as models
import time

class DriverAuthentication(rest_framework.authentication.BasicAuthentication):

    def authenticate_credentials(self, userid, password):
        """
        Authenticate the userid and password against username and password.
        """
        magento_user = models.DriverManagement.objects.filter(phone=userid)
        if len(magento_user) != 1:
            raise exceptions.AuthenticationFailed(('User inactive or deleted.'))

        magento_user = magento_user[0]

        # present in DB validate the password
        if password != magento_user.password:
            raise exceptions.AuthenticationFailed(('Invalid username/password.'))

        try:
            user = User.objects.get(username=magento_user.phone)
        except User.DoesNotExist as e:
            user = User.objects.create_user(
                        username=magento_user.phone,
                        password=magento_user.password)

        return (user, None)

