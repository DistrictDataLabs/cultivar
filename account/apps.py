# account.apps
# Application configuration for account
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 21:10:12 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Application configuration for account
"""

##########################################################################
## Imports
##########################################################################


from __future__ import unicode_literals

from django.apps import AppConfig

##########################################################################
## Configuration
##########################################################################


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        import account.signals
