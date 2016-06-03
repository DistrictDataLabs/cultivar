# trinket.celery
# Celery instance
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Jun 03 12:03:55 2016 -0700
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: celery.py [] allen.leis@gmail.com $

"""
Celery instance
"""

##########################################################################
## Imports
##########################################################################

import os

import dotenv
from celery import Celery

##########################################################################
## Helpers to find .env file
##########################################################################

PROJECT = os.path.dirname(os.path.dirname(__file__))
DOTENVF = os.path.join(PROJECT, '.env')

##########################################################################
## Celery
##########################################################################

## Load settings from environment and then import django settings
dotenv.read_dotenv(DOTENVF)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trinket.settings.production")
from django.conf import settings

# create celery object
app = Celery('trinket')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

# set celery to auto discovery tasks within the INSTALLED_APPS list
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


if __name__ == '__main__':
    app.start()
