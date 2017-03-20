import os
import django
import pytest

from django.conf import settings

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
# by default we move it to local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = True
    # If you have any test specific settings, you can declare them here,
    # e.g.
    # settings.PASSWORD_HASHERS = (
    #     'django.contrib.auth.hashers.MD5PasswordHasher',
    # )
    django.setup()
    # Note: In Django =< 1.6 you'll need to run this instead
    # settings.configure()


@pytest.yield_fixture(scope='session')
def django_db_setup():
    yield


import app.core.core.magento_api as mage
@pytest.fixture(scope="session")
def magento():
    conn = mage.Connector()
    return conn
