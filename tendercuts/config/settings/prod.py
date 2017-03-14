from .base import *

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
        'USER': 'root',
        'PASSWORD': '!qazmlp)5',
        'HOST': 'localhost',
        'PORT': '3306',

    },
    'magento': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'v2',
        'USER': 'root',
        'PASSWORD': '!qazmlp)5',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}

MAGENTO = {
    "url": "tendercuts.in",
    "port": 443,
    "username": "admin",
    "password": "Tendercuts123!",
    "endpoint": "/index.php/api/xmlrpc/",
    "proto": "https"
}
