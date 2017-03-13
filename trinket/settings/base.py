# trinket.settings.base
# The common Django settings for Trinket project
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Apr 01 23:17:27 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: base.py [] bbengfort@districtdatalabs.com $

"""
Django settings for Trinket project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os
import dj_database_url
from kombu import Exchange, Queue

from trinket.utils import htmlize
from django.conf import global_settings

##########################################################################
## Helper function for environmental settings
##########################################################################

def environ_setting(name, default=None):
    """
    Fetch setting from the environment- if not found, then this setting is
    ImproperlyConfigured.
    """
    if name not in os.environ and default is None:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "The {0} ENVVAR is not set.".format(name)
        )

    return os.environ.get(name, default)

##########################################################################
## Build Paths inside of project with os.path.join
##########################################################################

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY = os.path.dirname(PROJECT)

##########################################################################
## Secret settings - do not store!
##########################################################################

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ_setting("SECRET_KEY")

##########################################################################
## Database Settings
##########################################################################

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

##########################################################################
## Runtime settings
##########################################################################

## Debugging settings
## SECURITY WARNING: don't run with debug turned on in production!
DEBUG          = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

## Hosts
ALLOWED_HOSTS  = ["*"]
INTERNAL_IPS   = ('127.0.0.1', '198.168.1.10')

## WSGI Configuration
ROOT_URLCONF     = 'trinket.urls'
WSGI_APPLICATION = 'trinket.wsgi.application'

## Application definition
INSTALLED_APPS = (
    # Django apps
    'grappelli', # Must come before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third party apps
    'rest_framework',
    'django_gravatar',
    'storages',

    # Trinket apps
    'account',
    'dataset',
    'members',
    'organization',
    'trinket',
)

## Request Handling
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

## Internationalization
## https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

##########################################################################
## Content (Static, Media, Templates)
##########################################################################

## Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
            ],
        },
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/assets/'

STATICFILES_DIRS = (
    os.path.join(PROJECT, 'assets'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

##########################################################################
## AWS S3 Storage
##########################################################################
#if AWS env settings are present, then those settings will be used for storage.  Otherwise, the Django
#DEFAULT_FILE_STORAGE will be used, which is based on the MEDIA_ROOT setting
if environ_setting("AWS_ACCESS_KEY_ID", "") and environ_setting("AWS_SECRET_ACCESS_KEY", ""):
    DEFAULT_FILE_STORAGE    = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID       = environ_setting("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY   = environ_setting("AWS_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = environ_setting("AWS_STORAGE_BUCKET_NAME", "trinket-coffer")

##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'bbengfort@districtdatalabs.com'),
    ('Tony Ojeda', 'tojeda@districtdatalabs.com'),
    ('Rebecca Bilbro', 'rbilbro@districtdatalabs.com'),
)

SERVER_EMAIL    = 'DDL Admin <admin@districtdatalabs.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER      = environ_setting("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD  = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587
EMAIL_SUBJECT_PREFIX = '[TRINKET] '

##########################################################################
## CMS
##########################################################################

GRAPPELLI_ADMIN_TITLE = "DDL Trinket CMS"

##########################################################################
## Gravatar Configuration
##########################################################################

GRAVATAR_DEFAULT_SIZE   = 512
GRAVATAR_DEFAULT_IMAGE  = 'identicon'
GRAVATAR_DEFAULT_RATING = 'r'
GRAVATAR_ICON_SIZE      = 30

##########################################################################
## MarkupField Configuration
##########################################################################

MARKUP_FIELD_TYPES = (
    ('markdown', htmlize),
)

##########################################################################
## Social Authentication
##########################################################################

## Password validation
## https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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

## Support for Social Auth authentication backends
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

## Social authentication strategy
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

## Google-specific authentication keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = environ_setting("GOOGLE_OAUTH2_CLIENT_ID", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ_setting("GOOGLE_OAUTH2_CLIENT_SECRET", "")

## Domain whitelist
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = [
    'districtdatalabs.com',
]

LOGIN_REDIRECT_URL = "home"

## Error handling
SOCIAL_AUTH_LOGIN_ERROR_URL = "login"
SOCIAL_AUTH_GOOGLE_OAUTH2_SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

##########################################################################
## Django REST Framework
##########################################################################

REST_FRAMEWORK = {

    ## API Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    ## Default permissions to access the API
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    ## Pagination in the API
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'per_page',
    'MAX_PAGINATE_BY': 200,
}

##########################################################################
## Celery Configuration
##########################################################################

# Broker info
BROKER_HOST = environ_setting("AMQP_HOST", "localhost")
BROKER_PORT = 5672
BROKER_USER = environ_setting("AMQP_USER", "guest")
BROKER_PASSWORD = environ_setting("AMQP_PASSWORD", "")

# Result Backend
CELERY_RESULT_BACKEND = 'amqp'

# Serialization
CELERY_TASK_SERIALIZER     = 'json'
CELERY_RESULT_SERIALIZER   = 'json'
CELERY_ACCEPT_CONTENT      = ['json', 'yaml']

# Time related
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TIME_ZONE           ='America/New_York'
CELERY_ENABLE_UTC          = False

# Queue/Route related
CELERY_DEFAULT_QUEUE = environ_setting("CELERY_DEFAULT_QUEUE", 'trinket')
DEFAULT_EXCHANGE = Exchange(CELERY_DEFAULT_QUEUE, type='topic')

CELERY_QUEUES = (
    Queue(CELERY_DEFAULT_QUEUE, DEFAULT_EXCHANGE, routing_key=CELERY_DEFAULT_QUEUE),
)
