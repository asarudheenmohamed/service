from .base import *
from .celeryconfig import *

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
        'NAME': 'v3_5',
        'USER': 'root',
        'PASSWORD': '!qazmlp)5',
        'HOST': 'localhost',
        'PORT': '3306',

    },
    'erp': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tendercuts',
        'USER': 'odoo',
        'PASSWORD': 'odoo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MAGENTO = {
    "url": "staging.tendercuts.in",
    "port": 443,
    "username": "admin",
    "password": "Tendercuts123!",
    "endpoint": "/v3/website/index.php/api/xmlrpc/",
    "servicepoint": "/tendercuts-site/index.php/servicelayer/",
    "proto": "https"
}

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

INTERNAL_IPS = (
    '127.0.0.1'
)


CELERY_MAIL = {
    'sender_mail_id': "reports@tendercuts.in",
    'received_mail_id': ["varun@tendercuts.in", "asarudheen@tendercuts.in", "naveen@tendercuts.in"]
}

INSTALLED_APPS += ("debug_toolbar", "django_extensions")
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

INTERNAL_IPS = (
    '127.0.0.1'
)

PAYMENT = {
    "SIMPL": {
        "secret": "887b47b4aa1adffbdfa49e0c7fb0cc04",
        "url": "https://sandbox-api.getsimpl.com"
    },
    "RZP": {
        "merchant_id": "6gzz9v5B2a354o",
        "id": "rzp_test_CHbBWl0VBUXzyU",
        "secret": "CGnPUkQSpWevFi33ElQY7rjI",
        "url": ""
    },
    "JUSPAY": {
        "merchant_id": "tendercuts",
        "id": "0F38CA55EAA0492987E8B5FB5635D223",
        "secret": "C8B21475421D4A14AE78A825344B7E65",
        "url": "https://sandbox.juspay.in/card/tokenize",
        "return_url": "https://staging.tendercuts.in:82/payment/juspay",
        "environment": "sandbox",
        "web_success_url": "https://staging.tendercuts.in:83/success?orderId={}",
        "web_failure_url": "https://staging.tendercuts.in:83/payment-retry?orderId={}"
    },
    "PAYU": {
        "url": "https://test.payu.in/",
        "merchant_id": "U6KiaG3M",
        "secret": "xV0BSL"
    },
    "PAYTM": {
        "url": "https://pguat.paytm.com",
        "merchant_id": "Tender34302647116050",
        "merchant_website": "olehcsweb",
        "secret": "5JULNc!gvrfouxyL",
        "environment": "Sandbox"
    }
}

MAGE_ATTRS = {
    'GEOHASH': 245,
    'LATITUDE': 239,
    'LONGITUDE': 237,
    'STREET': 25,
    'PINCODE': 30,
    'IS_VERIFIED': 244
}

FLOCK_ENDPOINTS = {
    'APPROVE_INV_REQ': 'https://staging.tendercuts.in:82/store_manager/inv_request/approve'
}

REFERRAL_RULE_ID = 118
