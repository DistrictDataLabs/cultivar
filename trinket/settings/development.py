# trinket.settings.development
# The Django settings for Trinket in development
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Apr 01 23:19:25 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: development.py [] bbengfort@districtdatalabs.com $

"""
The Django settings for TopicMaps in development
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Secret Key doesn't matter in Dev
SECRET_KEY       = 'ddl+zirks79p$y4&06v1n8au&svwv1v($*&ep%cnu=pwz+p%2qm@xrsb'

## Content
MEDIA_ROOT       = os.path.join(PROJECT, 'media')
STATIC_ROOT      = 'staticfiles'


## DBs
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'trinket'),
        'USER': environ_setting('DB_USER', 'postgres'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}