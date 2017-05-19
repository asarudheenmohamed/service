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
    "password": "(ZvfP5$7F?Q3u\dq",
    "endpoint": "/index.php/api/xmlrpc/",
    "proto": "https"
}

PAYMENT = {
    "SIMPL": {
        "secret": "887b47b4aa1adffbdfa49e0c7fb0cc04",
        "url": "https://api.getsimpl.com/"
    },
    "RZP": {
        "merchant_id": "6gzz9v5B2a354o",
        "id": "rzp_live_GnowTFwKbmjJAw",
        "secret": "rKZcwb0mSFk01WnyLhg4OeAg",
        "url": ""
    },
    "JUSPAY": {
        "merchant_id": "TenderCuts",
        "id": "12CC428E2EF843059C3EAC10AE14F06F",
        "secret": "7E93DB150C034DF79E5C21BB61D9D5EB",
        "url": "https://api.juspay.in/card/tokenize",
        "return_url": "https://api.tendercuts.in/payment/juspay",
        "environment": "production"
    }
}
