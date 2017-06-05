from .base import *

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
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',

    },

    # Localhost
    'magento': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbmaster',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }

    # Forwarding config
    # 'magento': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'v2',
    #         'USER': 'tcuser',
    #         'PASSWORD': 'oochahwielai9mahDah3',
    #         'HOST': '127.0.0.1',
    #         'PORT': '3307',
    #     }

}


INSTALLED_APPS += ("debug_toolbar", "django_extensions")
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

INTERNAL_IPS = (
    '127.0.0.1'
)

MAGENTO = {
    "url": "localhost",
    "port": 80,
    "username": "admin",
    "password": "Tendercuts123!",
    "endpoint": "/tendercuts-site/index.php/api/xmlrpc/",
    "proto": "http"
}


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
        "return_url": "http://staging.tendercuts.in:82/payment/juspay",
        "environment": "sandbox"
    }
}