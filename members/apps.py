# members.apps
# Describes the Members application for Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 10:41:24 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Describes the Members application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Members Config
##########################################################################

class MembersConfig(AppConfig):
    name = 'members'
    verbose_name = "Member Profiles"

    def ready(self):
        import members.signals
