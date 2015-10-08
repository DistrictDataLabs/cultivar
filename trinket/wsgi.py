# trinket.wsgi
# WSGI config for the DDL Trinket project.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 21 14:52:45 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: wsgi.py [] benjamin@bengfort.com $

"""
WSGI config for Trinket project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

##########################################################################
## WSGI Configuration
##########################################################################

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trinket.settings.production")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
