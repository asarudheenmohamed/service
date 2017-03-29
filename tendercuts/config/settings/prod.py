from .base import *
from .celeryconfig import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'services',
        'USER': 'tcuser',
        'PASSWORD': 'aiz8Ahquiey9ieV',
        'HOST': 'dbmaster',
        'PORT': '3306',

    },
    'magento': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'v2',
        'USER': 'tcuser',
        'PASSWORD': 'aiz8Ahquiey9ieV',
        'HOST': 'dbmaster',
        'PORT': '3306',

    }
}

MAGENTO = {
    "url": "tendercuts.in",
    "port": 443,
    "username": "admin",
    "password": "fp/(%488kdjm",
    "endpoint": "/index.php/api/xmlrpc/",
    "proto": "https"
}
