"""
Django settings for tendercuts project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pb#ie&)83+5_0-yo0@62@sx2kr0l=&j4u2q+%axw(@3=*#0^qk'

ALLOWED_HOSTS = [
    "testserver",
    "localhost",
    "staging.tendercuts.in",
    "api.tendercuts.in"]

# AUTH_USER_MODEL = 'driver.DriverManagement'
AUTHENTICATION_BACKENDS = (
    # 'driver.auth.DriverAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
DATABASE_ROUTERS = ['config.db.DBRouter']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'app.core',
    'app.driver',
    'app.login',
    'app.sale_order',
    'app.inventory',
    'app.payment',
    'app.geohashing',
    'app.rating'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'driver.auth.DriverAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # ...
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join("/var/log/django", 'tendercuts.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'invlogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join("/var/log/django/inventory", 'inventory.log'),
            'when': 'midnight',  # 15MB
            'interval': 1,
            'formatter': 'verbose'
        },
        'driverlogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join("/var/log/django/driver", 'driver.log'),
            'when': 'midnight',  # 15MB
            'interval': 1,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'app.inventory': {
            'handlers': ['invlogfile', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'app.driver': {
            'handlers': ['driverlogfile', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Anything
        '': {
            'handlers': ['applogfile', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

ROOT_URLCONF = 'config.urls'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = ('.*', )

TEMPLATE_DIR_PATH = os.path.realpath("template")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(TEMPLATE_DIR_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CDN = "https://cdn1.tendercuts.in"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'


# application specific: Communication
# Deprecated:
OLD_SMS_GATEWAY = {
    "KEY": "A03daa52993fe5f1f3384925de5826b30",
    "SENDER_ID": "TENDER",
    "ENDPOINT": "http://alerts.synicsys.com/api/v4/"
}

SMS_GATEWAY = {
    "KEY": "152377Awdd5u4YpFi5917274f",
    "SENDER_ID": "TENDER",
    "ENDPOINT": "https://control.msg91.com/api/sendhttp.php",
    "RESENDPOINT": "http://api.msg91.com/api/retryotp.php",
    "ROUTE": 4,
    "COUNTRY": 91
}

MAIL_GATEWAY = {
    "TC_USER": "reports@tendercuts.in",
    "TC_PASS": "D%6Byz6+no;Dhgv2"
}


FRESHDESK = {
    "PASSWORD": "tendercuts1234",
    "CC_EMAILS": ['liza@tendercuts.in'],
    "KEY": "UovHZV5Glhiw5YOHIP0Q",
    "TICKETS_CREATE": {
        "ENDPOINT": "https://tendercuts.freshdesk.com/api/v2/tickets",
        "PRIORITY": {'LOW': 1, "MEDIUM": 2, 'HIGH': 3, "URGENT": 4},
        "STATUS": {'OPEN': 2, 'PENDING': 3, "RESOLVED": 4, "CLOSED": 5},
        "SOURCE": {"EMAIL": 1, "PORTAL": 2, "PHONE": 3, "CHAT": 7},
        "TYPE": "Internal Team",

    }
}

GOOGLE_MAP_DISTANCE_API = {
    "KEY": "AIzaSyCQK2O4AMogjO323B-6btf9f2krVWST3bU"
}

# porur and mmda latitude and longitude
STORE_LAT_LONG = {
    8: (13.082976, 80.171193),

    5: (13.041706, 80.176288)
}


# value first new ventor
VALUE_FIRST_SMS_GATEWAY = {
    "ENDPOINT": "http://203.212.70.200/smpp/sendsms",
    "USERNAME": "gfmhttp",
    "PASSWORD": "9823opas",
    "FROM": "TNDCTS",
    "GUID": "b637f10f-5acb-4f2e-8408-d6cfbf51ceb9"
}

ORDER_MEDIUM = {
    'POS': 4
}

SMS_TEMPLATES = {
    'payment_pending_to_cancel': 'your order #{} has been Cancelled.',
    'canceled': 'Dear Customer Your Order No.#{}. has been Cancelled. We are sorry to have missed you this time. Do call us again for fresh, juicy and tender choices from Tender Cuts. Looking forward to serving you! Tendercuts.in',
    'pending': 'Thank you for your trust in Tender Cuts. Your fresh, juicy and tender choice is noted and your order id is #{}. We will keep you updated on progress',
    'out_delivery': "Your order #{}, is now out for delivery. Have a great meal Wish to serve you again!",
    'processing': "We have started to process Your #{},we will notify you,when we start to deliver.Tendercut.in-Farm Fresh Meats.",
    'complete': "Thanks for choosing Tendercuts.Your order has been successfully delivered!.please give a missed call to rate our quality of the product.Like it-7097299492 Disliked it-7097299569",

    'retail_complete': "Thanks for choosing Tendercuts. Hope you had a great meal! Please give a missed call to rate our quality of the product. Like it-7097299492 Disliked it-7097299569",

    'payment_confirmation': "Payment for order #{} is now confirmed, we will notify you when we start to deliver.",
    'payment_refunded': "Payment alert: Payment for order #{} has been refunded and will reflect in your bank account in 5-7 working days.",
    'payment_pending': "Payment alert: Payment for order #{} is not complete and will take upto 15 mins to confirm with the bank. Sorry for the inconvenience."
}

# caching version
CACHE_DEFAULT_VERSION = 2

# app version
APP_VERSIONS = {
    "CUSTOMER_APP_VERSION": {
        "min_app_version": '1.9.2',
        "current_app_version": '2.0.3'
    },

    "DRIVER_APP_VERSION": {
        "min_app_version": '2.1.0',
        "current_app_version": '2.1.0'
    }
}

# Flock groups
GROUPS = {
    "TECH_SUPPORT": "g:5282d2270ce34879981964619491b654",
    "SCRUM": "g:5db92fa6225149be84183e4d79c19ada",
    "thoraipakkam": "g:c5c7e097f86f488190deda41e769fc0f",
    "valasarawakkam": "g:4b36aae148ac4a808e8e99f0bcb2d75e",
    "velachery": "g:443107c94d7341939bf7b9db2c0744e3",
    "mogappair": "g:823d501a91a541f9a6e53d183fc55f79",
    "medavakkam": "g:a5daf77b4ee146f6a378a4b1bd798206",
    "adayar": "g:f4b98d63098243b9bf423ee8d89f7ef1",
}

FLOCK_AUTH = {
    'APP_ID': '293d68bb-7307-4774-8644-c962eebefcd8',
    'APP_SECRET': '7cffbef4-f106-46db-a410-a8b88528a9af',
    'ALGO': ['HS256']
}

