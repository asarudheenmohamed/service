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
    'magento': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbmaster',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}

INSTALLED_APPS += ("debug_toolbar", )
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

