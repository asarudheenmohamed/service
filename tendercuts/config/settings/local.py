from .base import *
from .celeryconfig import *

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


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

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)
INSTALLED_APPS += ("debug_toolbar", "django_extensions")
MIDDLEWARE += ("debug_panel.middleware.DebugPanelMiddleware", )

INTERNAL_IPS = (
    '127.0.0.1'
)

MAGENTO = {
    "url": "localhost",
    "port": 80,
    "username": "admin",
    "password": "Tendercuts123!",
    "endpoint": "/tendercuts-site/index.php/api/xmlrpc/",
    "servicepoint": "/tendercuts-site/index.php/servicelayer/",
    "proto": "http"
}

MOBILE_VERSION = {
    "min_app_version": '1.9.2',
    "current_app_version": '1.9.6'
}

DRIVER_APP_VERSION = {
    "min_app_version": '2.0.0',
    "current_app_version": '2.0.0'
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
        "return_url": "http://localhost:8000/payment/juspay",
        "environment": "sandbox"
    },
    "PAYU": {
        "url": "https://info.payu.in/",
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
